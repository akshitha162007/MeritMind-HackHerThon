from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from database import get_db
from models import Application, Candidate, JobDescription, EmotionBlindScore, User, Session as UserSession
from agents.emotion_blind import run_emotion_blind_analysis
from pydantic import BaseModel
import uuid
from datetime import datetime

router = APIRouter(prefix="/api/emotion-blind", tags=["emotion-blind"])

class CandidateTranscript(BaseModel):
    application_id: str
    transcript: str

class EmotionBlindRequest(BaseModel):
    jd_text: str
    candidates: list


def get_user_from_token(authorization: str = Header(None), db: Session = Depends(get_db)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")

    token = authorization.replace("Bearer ", "")
    session = db.query(UserSession).filter(
        UserSession.token == token,
        UserSession.expires_at > datetime.utcnow()
    ).first()

    if not session:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = db.query(User).filter(User.id == session.user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

@router.post("/analyze")
def analyze_emotion_blind(
    request: EmotionBlindRequest,
    current_user: User = Depends(get_user_from_token),
    db: Session = Depends(get_db)
):
    try:
        jd_text = request.jd_text
        candidates_input = request.candidates
        
        if not jd_text or not jd_text.strip():
            raise HTTPException(status_code=400, detail="Job description text is required")
        
        candidates_data = []
        for idx, candidate_input in enumerate(candidates_input):
            transcript = candidate_input.get("transcript", "")
            
            if not transcript or not transcript.strip():
                continue
            
            # Use index as blind_id for candidates without database records (direct text input)
            blind_id = candidate_input.get("blind_id") or f"Candidate {idx + 1}"
            app_id = candidate_input.get("application_id") or f"temp-{idx}"
            
            candidates_data.append({
                "application_id": app_id,
                "blind_id": blind_id,
                "transcript": transcript,
                "jd_text": jd_text
            })
        
        if not candidates_data:
            raise HTTPException(status_code=400, detail="No valid candidates found")
        
        results = run_emotion_blind_analysis(candidates_data)
        
        # Only save to database if application_ids are real (not temp)
        for result in results:
            if not result["application_id"].startswith("temp-"):
                existing = db.query(EmotionBlindScore).filter(
                    EmotionBlindScore.application_id == result["application_id"]
                ).first()
                
                if existing:
                    existing.transcript = result["transcript"]
                    existing.emotional_score = result["emotional_score"]
                    existing.semantic_score = result["semantic_score"]
                    existing.gap_score = result["gap_score"]
                    existing.bias_flagged = result["bias_flagged"]
                    existing.flag_reason = result["flag_reason"]
                else:
                    new_score = EmotionBlindScore(
                        id=str(uuid.uuid4()),
                        application_id=result["application_id"],
                        transcript=result["transcript"],
                        emotional_score=result["emotional_score"],
                        semantic_score=result["semantic_score"],
                        gap_score=result["gap_score"],
                        bias_flagged=result["bias_flagged"],
                        flag_reason=result["flag_reason"],
                        created_at=datetime.utcnow()
                    )
                    db.add(new_score)
        
        db.commit()
        
        return {
            "status": "success",
            "results": results
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/results/{jd_id}")
def get_emotion_blind_results(
    jd_id: str,
    current_user: User = Depends(get_user_from_token),
    db: Session = Depends(get_db)
):
    try:
        applications = db.query(Application).filter(Application.jd_id == jd_id).all()
        
        if not applications:
            return {
                "status": "success",
                "jd_id": jd_id,
                "results": []
            }
        
        results = []
        for app in applications:
            ebs = db.query(EmotionBlindScore).filter(EmotionBlindScore.application_id == app.id).first()
            candidate = db.query(Candidate).filter(Candidate.id == app.candidate_id).first()
            
            if ebs and candidate:
                results.append({
                    "application_id": app.id,
                    "candidate_id": candidate.id,
                    "blind_id": candidate.blind_id,
                    "transcript": ebs.transcript,
                    "emotional_score": ebs.emotional_score,
                    "semantic_score": ebs.semantic_score,
                    "gap_score": ebs.gap_score,
                    "bias_flagged": ebs.bias_flagged,
                    "flag_reason": ebs.flag_reason
                })
        
        return {
            "status": "success",
            "jd_id": jd_id,
            "results": results
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
def emotion_blind_health():
    return {
        "status": "ok",
        "feature": "EmotionBlind AI"
    }
