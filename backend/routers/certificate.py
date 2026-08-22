from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.responses import HTMLResponse, FileResponse
from sqlalchemy.orm import Session
from database import get_db
from models import User, Session as UserSession
from agents.certificate_generator import generate_certificate_html, generate_certificate_data
from pydantic import BaseModel
from datetime import datetime
import io

router = APIRouter(prefix="/api/certificate", tags=["certificate"])


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


class CertificateRequest(BaseModel):
    company_name: str
    original_jd: str
    variant_type: str  # "conservative", "balanced", "inclusive-first"
    original_bias_score: float
    rewritten_bias_score: float
    bias_matrix: dict = {}
    compliance_laws: list = []
    attraction_scores: dict = None
    resolved_biases: list = None


@router.post("/generate")
def generate_certificate(
    request: CertificateRequest,
    current_user: User = Depends(get_user_from_token),
    db: Session = Depends(get_db)
):
    """
    Generate a Bias Audit Certificate in HTML format.
    Can be viewed in browser or printed to PDF.
    """
    try:
        html_content = generate_certificate_html(
            company_name=request.company_name,
            recruiter_name=current_user.name or current_user.email,
            original_jd=request.original_jd,
            variant_type=request.variant_type,
            original_bias_score=request.original_bias_score,
            rewritten_bias_score=request.rewritten_bias_score,
            bias_matrix=request.bias_matrix,
            compliance_laws=request.compliance_laws,
            attraction_scores=request.attraction_scores,
            resolved_biases=request.resolved_biases
        )
        
        cert_data = generate_certificate_data(
            company_name=request.company_name,
            recruiter_name=current_user.name or current_user.email,
            original_jd=request.original_jd,
            variant_type=request.variant_type,
            original_bias_score=request.original_bias_score,
            rewritten_bias_score=request.rewritten_bias_score,
            bias_matrix=request.bias_matrix,
            compliance_laws=request.compliance_laws,
            attraction_scores=request.attraction_scores,
            resolved_biases=request.resolved_biases
        )
        
        return {
            "status": "success",
            "certificate_id": cert_data["certificate_id"],
            "html_content": html_content,
            "certificate_data": cert_data,
            "message": "Certificate generated successfully. Open the HTML content in a browser to view or print to PDF."
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-html")
def generate_certificate_html_only(
    request: CertificateRequest,
    current_user: User = Depends(get_user_from_token),
    db: Session = Depends(get_db)
):
    """
    Generate and return certificate as HTML response for direct viewing.
    """
    try:
        html_content = generate_certificate_html(
            company_name=request.company_name,
            recruiter_name=current_user.name or current_user.email,
            original_jd=request.original_jd,
            variant_type=request.variant_type,
            original_bias_score=request.original_bias_score,
            rewritten_bias_score=request.rewritten_bias_score,
            bias_matrix=request.bias_matrix,
            compliance_laws=request.compliance_laws,
            attraction_scores=request.attraction_scores,
            resolved_biases=request.resolved_biases
        )
        
        return HTMLResponse(content=html_content)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/preview")
def preview_certificate(
    request: CertificateRequest,
    current_user: User = Depends(get_user_from_token),
    db: Session = Depends(get_db)
):
    """
    Generate certificate data for preview without HTML rendering.
    """
    try:
        cert_data = generate_certificate_data(
            company_name=request.company_name,
            recruiter_name=current_user.name or current_user.email,
            original_jd=request.original_jd,
            variant_type=request.variant_type,
            original_bias_score=request.original_bias_score,
            rewritten_bias_score=request.rewritten_bias_score,
            bias_matrix=request.bias_matrix,
            compliance_laws=request.compliance_laws,
            attraction_scores=request.attraction_scores,
            resolved_biases=request.resolved_biases
        )
        
        return {
            "status": "success",
            "certificate": cert_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
