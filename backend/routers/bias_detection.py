from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models import User, Session as UserSession, JobDescription, BiasReport, IntersectionalBiasMatrix, Application
import uuid
from datetime import datetime, timezone
from agents.jd_bias_analyzer import analyze_jd_bias, generate_rewrite

router = APIRouter(prefix="/api/bias", tags=["bias"])

class AnalyzeRequest(BaseModel):
    pass

class RewriteRequest(BaseModel):
    variant: str = "balanced"

def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)):
    """Extract user from Authorization header."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid Authorization header")
    token = authorization.split(" ", 1)[1]
    session = db.query(UserSession).filter(
        UserSession.token == token,
        UserSession.expires_at > datetime.now(timezone.utc)
    ).first()
    if not session:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    user = db.query(User).filter(User.id == session.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return user

@router.post("/analyze/{jd_id}")
def analyze_jd(
    jd_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Run bias analysis on a job description (RECRUITER/ADMIN only)."""
    
    if current_user.role not in ["recruiter", "admin"]:
        raise HTTPException(status_code=403, detail="Only recruiters can run bias analysis")
    
    try:
        jd_uuid = uuid.UUID(jd_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid JD ID format")
    
    jd = db.query(JobDescription).filter(JobDescription.id == jd_uuid).first()
    if not jd:
        raise HTTPException(status_code=404, detail="Job description not found")
    
    if jd.recruiter_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="You can only analyze your own job descriptions")
    
    bias_result = analyze_jd_bias(jd.raw_text)
    
    db.query(BiasReport).filter(BiasReport.jd_id == jd_uuid).delete()
    db.query(IntersectionalBiasMatrix).filter(
        IntersectionalBiasMatrix.report_id.in_(
            db.query(BiasReport.id).filter(BiasReport.jd_id == jd_uuid)
        )
    ).delete()
    
    bias_report_ids = []
    for flag in bias_result.get("bias_flags", []):
        report = BiasReport(
            id=uuid.uuid4(),
            jd_id=jd_uuid,
            bias_type=flag.get("axis", "unknown"),
            trigger_phrase=flag.get("trigger_phrase", ""),
            severity=flag.get("severity", 5),
            axis=flag.get("axis", "unknown"),
            intersectional_axes=flag.get("intersectional_axes", []),
            suggestion=flag.get("suggested_rewrite", "")
        )
        db.add(report)
        db.flush()
        bias_report_ids.append(report.id)
    
    for matrix_item in bias_result.get("matrix", []):
        if bias_report_ids:
            matrix = IntersectionalBiasMatrix(
                id=uuid.uuid4(),
                report_id=bias_report_ids[0],
                axis_row=matrix_item.get("axis_row", ""),
                axis_col=matrix_item.get("axis_col", ""),
                score=matrix_item.get("score", 0),
                trigger=matrix_item.get("trigger_phrase", "")
            )
            db.add(matrix)
    
    jd.bias_score = bias_result.get("overall_bias_score", 0)
    jd.status = "analyzed"
    db.commit()
    
    return {
        "jd_id": str(jd_uuid),
        "overall_bias_score": bias_result.get("overall_bias_score", 0),
        "bias_flags": bias_result.get("bias_flags", []),
        "matrix": bias_result.get("matrix", []),
        "summary": bias_result.get("summary", ""),
        "analyzed_at": datetime.now(timezone.utc).isoformat()
    }

@router.get("/report/{jd_id}")
def get_bias_report(
    jd_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get bias report (RECRUITER sees full, CANDIDATE sees limited)."""
    
    try:
        jd_uuid = uuid.UUID(jd_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid JD ID format")
    
    jd = db.query(JobDescription).filter(JobDescription.id == jd_uuid).first()
    if not jd:
        raise HTTPException(status_code=404, detail="Job description not found")
    
    bias_reports = db.query(BiasReport).filter(BiasReport.jd_id == jd_uuid).all()
    
    if current_user.role == "candidate":
        return {
            "jd_title": jd.title,
            "jd_company": "Unknown",
            "overall_bias_score": jd.bias_score,
            "bias_checked": len(bias_reports) > 0,
            "summary": "This job description has been reviewed for bias and inclusivity" if len(bias_reports) > 0 else None,
            "total_flags": len(bias_reports)
        }
    
    if current_user.role not in ["recruiter", "admin"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    if jd.recruiter_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="You can only view your own job descriptions")
    
    matrix_entries = []
    for report in bias_reports:
        matrices = db.query(IntersectionalBiasMatrix).filter(
            IntersectionalBiasMatrix.report_id == report.id
        ).all()
        matrix_entries.extend([
            {
                "axis_row": m.axis_row,
                "axis_col": m.axis_col,
                "score": m.score,
                "trigger_phrase": m.trigger
            }
            for m in matrices
        ])
    
    return {
        "jd_id": str(jd_uuid),
        "jd_title": jd.title,
        "overall_bias_score": jd.bias_score,
        "bias_flags": [
            {
                "axis": r.axis,
                "trigger_phrase": r.trigger_phrase,
                "severity": r.severity,
                "intersectional_axes": r.intersectional_axes,
                "suggestion": r.suggestion
            }
            for r in bias_reports
        ],
        "matrix": matrix_entries,
        "summary": f"Detected {len(bias_reports)} bias indicators",
        "analyzed_at": bias_reports[0].created_at.isoformat() if bias_reports else None
    }

@router.post("/rewrite/{jd_id}")
def rewrite_jd(
    jd_id: str,
    req: RewriteRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate rewritten JD (RECRUITER/ADMIN only)."""
    
    if current_user.role not in ["recruiter", "admin"]:
        raise HTTPException(status_code=403, detail="Only recruiters can rewrite job descriptions")
    
    try:
        jd_uuid = uuid.UUID(jd_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid JD ID format")
    
    jd = db.query(JobDescription).filter(JobDescription.id == jd_uuid).first()
    if not jd:
        raise HTTPException(status_code=404, detail="Job description not found")
    
    if jd.recruiter_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="You can only rewrite your own job descriptions")
    
    bias_reports = db.query(BiasReport).filter(BiasReport.jd_id == jd_uuid).all()
    if not bias_reports:
        raise HTTPException(status_code=400, detail="Run bias analysis first before rewriting")
    
    bias_report_dict = {
        "overall_bias_score": jd.bias_score,
        "bias_flags": [
            {
                "axis": r.axis,
                "trigger_phrase": r.trigger_phrase,
                "severity": r.severity,
                "intersectional_axes": r.intersectional_axes,
                "suggested_rewrite": r.suggestion
            }
            for r in bias_reports
        ]
    }
    
    variant = req.variant if req.variant in ["conservative", "balanced", "aggressive"] else "balanced"
    rewrite_result = generate_rewrite(jd.raw_text, bias_report_dict, variant)
    
    jd.inclusive_text = rewrite_result.get("rewritten_jd", jd.raw_text)
    jd.bias_score = rewrite_result.get("new_bias_score", jd.bias_score)
    jd.status = "rewritten"
    db.commit()
    
    original_score = bias_report_dict.get("overall_bias_score", 0)
    new_score = rewrite_result.get("new_bias_score", 0)
    improvement = original_score - new_score
    
    return {
        "jd_id": str(jd_uuid),
        "variant": variant,
        "original_jd": jd.raw_text,
        "rewritten_jd": rewrite_result.get("rewritten_jd", ""),
        "changes": rewrite_result.get("changes", []),
        "original_bias_score": original_score,
        "new_bias_score": new_score,
        "improvement": improvement
    }

@router.get("/jd-list")
def get_jd_list(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get list of recruiter's JDs with bias status (RECRUITER only)."""
    
    if current_user.role != "recruiter":
        raise HTTPException(status_code=403, detail="Only recruiters can view job descriptions")
    
    jds = db.query(JobDescription).filter(JobDescription.recruiter_id == current_user.id).all()
    
    result = []
    for jd in jds:
        bias_reports = db.query(BiasReport).filter(BiasReport.jd_id == jd.id).all()
        result.append({
            "id": str(jd.id),
            "title": jd.title,
            "company": "Unknown",
            "has_bias_report": len(bias_reports) > 0,
            "overall_bias_score": jd.bias_score,
            "has_rewrite": jd.inclusive_text is not None,
            "status": "draft"
        })
    
    return result

@router.get("/candidate-view/{jd_id}")
def get_candidate_bias_view(
    jd_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get limited bias info for candidate (CANDIDATE only)."""
    
    if current_user.role != "candidate":
        raise HTTPException(status_code=403, detail="Only candidates can view this")
    
    try:
        jd_uuid = uuid.UUID(jd_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid JD ID format")
    
    application = db.query(Application).filter(
        Application.jd_id == jd_uuid,
        Application.candidate_id == current_user.id
    ).first()
    
    if not application:
        raise HTTPException(status_code=403, detail="You have not applied to this job")
    
    jd = db.query(JobDescription).filter(JobDescription.id == jd_uuid).first()
    if not jd:
        raise HTTPException(status_code=404, detail="Job description not found")
    
    bias_reports = db.query(BiasReport).filter(BiasReport.jd_id == jd_uuid).all()
    
    return {
        "jd_title": jd.title,
        "bias_checked": len(bias_reports) > 0,
        "overall_bias_score": jd.bias_score if len(bias_reports) > 0 else None,
        "summary": "This job description has been reviewed for bias and inclusivity by Merit Mind AI" if len(bias_reports) > 0 else None,
        "message": "This job description has been reviewed for bias and inclusivity by Merit Mind AI"
    }
