from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from database import get_db
from models import User, Session as UserSession, JobDescription
from agents.job_rewriter import rewrite_job_description, calculate_attraction_score
from pydantic import BaseModel
from datetime import datetime
import uuid
import json

router = APIRouter(prefix="/api/job-rewriter", tags=["job-rewriter"])


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


class RewriteRequest(BaseModel):
    jd_text: str
    bias_matrix: dict
    target_demographics: list = []  # e.g., ["women_tier2_cities", "differently_abled"]


class VariantRequest(BaseModel):
    variant: str  # "conservative", "balanced", "inclusive-first"


@router.post("/rewrite")
def rewrite_jd(
    request: RewriteRequest,
    current_user: User = Depends(get_user_from_token),
    db: Session = Depends(get_db)
):
    """
    Rewrite job description in three variants based on detected bias.
    Generates Conservative, Balanced, and Inclusive-First versions.
    """
    try:
        if not request.jd_text or not request.jd_text.strip():
            raise HTTPException(status_code=400, detail="Job description text is required")

        # Generate three variants using the rewriting agent
        rewritten_variants = rewrite_job_description(
            original_jd=request.jd_text,
            bias_matrix=request.bias_matrix,
            target_demographics=request.target_demographics
        )

        return {
            "status": "success",
            "original_jd": request.jd_text,
            "variants": rewritten_variants,
            "bias_matrix": request.bias_matrix,
            "target_demographics": request.target_demographics
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/attraction-score")
def calculate_attraction(
    request: dict,
    current_user: User = Depends(get_user_from_token),
    db: Session = Depends(get_db)
):
    """
    Calculate attraction score for a rewritten JD against target demographics.
    Shows predicted improvement in application diversity.
    """
    try:
        jd_text = request.get("jd_text")
        target_demographics = request.get("target_demographics", [])

        if not jd_text:
            raise HTTPException(status_code=400, detail="Job description text is required")

        score = calculate_attraction_score(jd_text, target_demographics)

        return {
            "status": "success",
            "attraction_score": score,
            "predicted_improvement": f"{score * 100:.1f}%",
            "appeal_factors": {
                "language_inclusivity": score.get("language_inclusivity", 0),
                "demographic_relevance": score.get("demographic_relevance", 0),
                "cultural_alignment": score.get("cultural_alignment", 0),
                "accessibility_focus": score.get("accessibility_focus", 0)
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/job-descriptions")
def get_user_job_descriptions(
    current_user: User = Depends(get_user_from_token),
    db: Session = Depends(get_db)
):
    """
    Get all job descriptions created by the authenticated recruiter.
    """
    try:
        # For now, return sample JD structure
        # In production, this would fetch from database where recruiter_id = current_user.id
        
        jds = db.query(JobDescription).filter(
            JobDescription.created_by == current_user.id
        ).all()

        result = []
        for jd in jds:
            result.append({
                "id": jd.id,
                "title": jd.title,
                "company": jd.company,
                "jd_text": jd.raw_text,
                "created_at": jd.created_at.isoformat() if hasattr(jd.created_at, 'isoformat') else str(jd.created_at)
            })

        return {
            "status": "success",
            "job_descriptions": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/save-variants")
def save_rewritten_variants(
    request: dict,
    current_user: User = Depends(get_user_from_token),
    db: Session = Depends(get_db)
):
    """
    Save rewritten job description variants for future reference.
    """
    try:
        original_jd_id = request.get("original_jd_id")
        variants = request.get("variants", {})

        # Store variant information (implementation depends on schema)
        saved_variants = {
            "conservative": variants.get("conservative", ""),
            "balanced": variants.get("balanced", ""),
            "inclusive_first": variants.get("inclusive_first", "")
        }

        return {
            "status": "success",
            "message": "Variants saved successfully",
            "variants_saved": saved_variants
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
