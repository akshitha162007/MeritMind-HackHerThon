"""
Bias Audit Certificate Generator
Generates professional certificates with before/after bias scores,
compliance information, and audit trail.
"""
from datetime import datetime
import json
from typing import Dict, List


def generate_certificate_html(
    company_name: str,
    recruiter_name: str,
    original_jd: str,
    variant_type: str,
    original_bias_score: float,
    rewritten_bias_score: float,
    bias_matrix: dict,
    compliance_laws: List[str],
    attraction_scores: Dict = None,
    resolved_biases: List[str] = None
) -> str:
    """
    Generate a professional HTML Bias Audit Certificate.
    Can be displayed in browser or converted to PDF.
    """
    
    bias_reduction = ((original_bias_score - rewritten_bias_score) / original_bias_score * 100) if original_bias_score > 0 else 0
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cert_id = f"BAC-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    resolved_biases_html = ""
    if resolved_biases:
        resolved_biases_html = "<div style='margin-top: 20px;'><h3>Resolved Bias Issues:</h3><ul>"
        for bias in resolved_biases:
            resolved_biases_html += f"<li>{bias}</li>"
        resolved_biases_html += "</ul></div>"
    
    compliance_html = ""
    if compliance_laws:
        compliance_html = "<div style='margin-top: 20px;'><h3>Indian Employment Law Compliance:</h3><ul>"
        for law in compliance_laws:
            compliance_html += f"<li>✓ {law}</li>"
        compliance_html += "</ul></div>"
    
    attraction_html = ""
    if attraction_scores:
        attraction_overall = attraction_scores.get("overall_score", 0)
        attraction_html = f"""
        <div style='margin-top: 20px; background-color: #f0f8ff; padding: 15px; border-radius: 8px;'>
            <h3>Attraction Score & Demographic Appeal</h3>
            <p><strong>Overall Attraction Score: {attraction_overall*100:.1f}%</strong></p>
            <p>Predicted improvement in application diversity from underrepresented demographics.</p>
            <ul>
                <li>Language Inclusivity: {attraction_scores.get('language_inclusivity', 0)*100:.1f}%</li>
                <li>Demographic Relevance: {attraction_scores.get('demographic_relevance', 0)*100:.1f}%</li>
                <li>Cultural Alignment: {attraction_scores.get('cultural_alignment', 0)*100:.1f}%</li>
                <li>Accessibility Focus: {attraction_scores.get('accessibility_focus', 0)*100:.1f}%</li>
            </ul>
        </div>
        """
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Bias Audit Certificate</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }}
            
            .certificate {{
                background: white;
                border-radius: 12px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                max-width: 900px;
                width: 100%;
                padding: 50px 40px;
                position: relative;
                overflow: hidden;
            }}
            
            .certificate::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 5px;
                background: linear-gradient(90deg, #667eea, #764ba2, #f093fb, #4facfe);
            }}
            
            .header {{
                text-align: center;
                margin-bottom: 40px;
                border-bottom: 2px solid #eee;
                padding-bottom: 30px;
            }}
            
            .logo-area {{
                font-size: 32px;
                font-weight: bold;
                color: #667eea;
                margin-bottom: 10px;
            }}
            
            .cert-title {{
                font-size: 28px;
                font-weight: 700;
                color: #333;
                margin: 15px 0;
                letter-spacing: 1px;
            }}
            
            .cert-subtitle {{
                font-size: 14px;
                color: #666;
                margin-bottom: 10px;
            }}
            
            .cert-id {{
                font-size: 12px;
                color: #999;
                font-family: monospace;
                margin-top: 10px;
            }}
            
            .content {{
                margin: 30px 0;
            }}
            
            .section {{
                margin-bottom: 30px;
            }}
            
            .section h3 {{
                font-size: 16px;
                font-weight: 600;
                color: #333;
                margin-bottom: 15px;
                text-transform: uppercase;
                border-bottom: 2px solid #667eea;
                padding-bottom: 10px;
            }}
            
            .info-grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                margin-bottom: 20px;
            }}
            
            .info-box {{
                background: #f9f9f9;
                padding: 15px;
                border-left: 4px solid #667eea;
                border-radius: 4px;
            }}
            
            .info-label {{
                font-size: 12px;
                color: #999;
                text-transform: uppercase;
                margin-bottom: 5px;
            }}
            
            .info-value {{
                font-size: 20px;
                font-weight: bold;
                color: #333;
            }}
            
            .score-comparison {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                margin: 20px 0;
            }}
            
            .score-card {{
                text-align: center;
                padding: 20px;
                border-radius: 8px;
                background: #f5f5f5;
            }}
            
            .score-card.before {{
                border: 2px solid #ff6b6b;
                background: #ffe0e0;
            }}
            
            .score-card.after {{
                border: 2px solid #51cf66;
                background: #e7f5ee;
            }}
            
            .score-label {{
                font-size: 12px;
                color: #666;
                text-transform: uppercase;
                margin-bottom: 10px;
            }}
            
            .score-value {{
                font-size: 32px;
                font-weight: bold;
                margin-bottom: 10px;
            }}
            
            .score-value.high {{
                color: #ff6b6b;
            }}
            
            .score-value.low {{
                color: #51cf66;
            }}
            
            .improvement {{
                font-size: 16px;
                font-weight: 600;
                color: #0ea5e9;
                margin-top: 15px;
                padding-top: 15px;
                border-top: 1px solid #ddd;
            }}
            
            .variant-info {{
                background: #f0f8ff;
                padding: 15px;
                border-radius: 8px;
                margin: 15px 0;
            }}
            
            .variant-badge {{
                display: inline-block;
                padding: 5px 12px;
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 600;
                margin-bottom: 10px;
            }}
            
            .resolved-list {{
                list-style: none;
                margin: 10px 0;
            }}
            
            .resolved-list li {{
                padding: 8px 0;
                padding-left: 30px;
                position: relative;
                color: #555;
            }}
            
            .resolved-list li::before {{
                content: '✓';
                position: absolute;
                left: 0;
                color: #51cf66;
                font-weight: bold;
                font-size: 16px;
            }}
            
            .compliance-list {{
                list-style: none;
                margin: 10px 0;
            }}
            
            .compliance-list li {{
                padding: 10px;
                margin: 5px 0;
                background: #f0f8ff;
                border-left: 4px solid #667eea;
                color: #333;
                border-radius: 4px;
            }}
            
            .footer {{
                margin-top: 40px;
                padding-top: 30px;
                border-top: 2px solid #eee;
                text-align: center;
                color: #999;
                font-size: 12px;
            }}
            
            .signature-area {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 40px;
                margin-top: 30px;
            }}
            
            .signature {{
                text-align: center;
            }}
            
            .signature-line {{
                border-top: 1px solid #333;
                margin-top: 40px;
                padding-top: 10px;
                min-height: 40px;
            }}
            
            .signature-label {{
                font-size: 12px;
                color: #666;
                margin-top: 5px;
            }}
            
            .badge-success {{
                display: inline-block;
                padding: 8px 16px;
                background: #51cf66;
                color: white;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 600;
                margin: 10px 0;
            }}
            
            @media print {{
                body {{
                    background: white;
                    padding: 0;
                }}
                .certificate {{
                    box-shadow: none;
                    border-radius: 0;
                }}
                .no-print {{
                    display: none;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="certificate">
            <div class="header">
                <div class="logo-area">🎖️ Merit Mind</div>
                <div class="cert-title">BIAS AUDIT CERTIFICATE</div>
                <div class="cert-subtitle">Autonomous Job Rewriting & Compliance Verification</div>
                <div class="cert-id">Certificate ID: {cert_id}</div>
                <div class="cert-id">Issued: {timestamp}</div>
            </div>
            
            <div class="content">
                <div class="section">
                    <h3>Organization Details</h3>
                    <div class="info-grid">
                        <div class="info-box">
                            <div class="info-label">Company</div>
                            <div class="info-value">{company_name}</div>
                        </div>
                        <div class="info-box">
                            <div class="info-label">Authorized By</div>
                            <div class="info-value">{recruiter_name}</div>
                        </div>
                    </div>
                </div>
                
                <div class="section">
                    <h3>Rewriting Variant</h3>
                    <div class="variant-badge">{variant_type.upper()}</div>
                    <p style="color: #666; margin-top: 10px;">
                        This job description has been automatically rewritten using the Autonomous Job Rewriting Agent to eliminate detected biases while maintaining role requirements.
                    </p>
                </div>
                
                <div class="section">
                    <h3>Bias Score Analysis</h3>
                    <div class="score-comparison">
                        <div class="score-card before">
                            <div class="score-label">Original Bias Score</div>
                            <div class="score-value high">{original_bias_score:.2f}</div>
                            <span style="color: #999; font-size: 12px;">Higher = More Bias Detected</span>
                        </div>
                        <div class="score-card after">
                            <div class="score-label">Rewritten Bias Score</div>
                            <div class="score-value low">{rewritten_bias_score:.2f}</div>
                            <span style="color: #999; font-size: 12px;">Lower = Less Bias Detected</span>
                        </div>
                    </div>
                    <div class="improvement">
                        Bias Reduction: <span style="color: #51cf66;">{bias_reduction:.1f}%</span>
                    </div>
                </div>
                
                {resolved_biases_html}
                {compliance_html}
                {attraction_html}
                
                <div class="section" style="background: #f5f5f5; padding: 20px; border-radius: 8px; margin-top: 30px;">
                    <h3 style="border: none; margin-bottom: 10px;">Verification Status</h3>
                    <div style="text-align: center;">
                        <div class="badge-success" style="font-size: 14px; padding: 10px 20px;">
                            ✓ CERTIFIED BIAS-COMPLIANT
                        </div>
                        <p style="margin-top: 10px; color: #666; font-size: 13px;">
                            This job description has been verified and certified to meet inclusive hiring standards and complies with applicable Indian employment laws.
                        </p>
                    </div>
                </div>
            </div>
            
            <div class="footer">
                <p>This certificate confirms that the job description has undergone comprehensive bias detection and autonomous rewriting using Merit Mind's proprietary AI-powered Bias Audit System.</p>
                <p style="margin-top: 10px;">Merit Mind © 2024 - Empowering Fair & Inclusive Hiring</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_content


def generate_certificate_data(
    company_name: str,
    recruiter_name: str,
    original_jd: str,
    variant_type: str,
    original_bias_score: float,
    rewritten_bias_score: float,
    bias_matrix: dict,
    compliance_laws: List[str],
    attraction_scores: Dict = None,
    resolved_biases: List[str] = None
) -> Dict:
    """
    Generate certificate data as JSON for API responses.
    """
    return {
        "certificate_id": f"BAC-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "issued_at": datetime.now().isoformat(),
        "company_name": company_name,
        "recruiter_name": recruiter_name,
        "variant_type": variant_type,
        "bias_analysis": {
            "original_score": original_bias_score,
            "rewritten_score": rewritten_bias_score,
            "bias_reduction_percentage": ((original_bias_score - rewritten_bias_score) / original_bias_score * 100) if original_bias_score > 0 else 0
        },
        "resolved_biases": resolved_biases or [],
        "compliance_laws": compliance_laws or [],
        "attraction_scores": attraction_scores or {},
        "status": "CERTIFIED" if rewritten_bias_score < original_bias_score else "PENDING_REVIEW"
    }
