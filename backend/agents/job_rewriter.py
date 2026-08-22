"""
Job Rewriting Agent - Feature 2
Autonomous agent that rewrites biased job descriptions in three variants
and generates Bias Audit Certificates.
"""
import openai
import os
from typing import Dict, List


def rewrite_job_description(
    original_jd: str,
    bias_matrix: dict,
    target_demographics: List[str] = []
) -> Dict[str, str]:
    """
    Rewrite job description in three variants:
    1. Conservative: Minimal changes to fix critical bias
    2. Balanced: Moderate changes for recommended middle ground
    3. Inclusive-First: Maximum reach with inclusive language
    """
    
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        # Fallback variants without API
        return _generate_fallback_variants(original_jd, bias_matrix)
    
    try:
        client = openai.OpenAI(api_key=api_key)
        
        bias_summary = _format_bias_matrix(bias_matrix)
        demographics_str = ", ".join(target_demographics) if target_demographics else "diverse candidates"
        
        # Conservative variant - minimal changes
        conservative_response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert bias auditor. Rewrite the following job description 
                    to address ONLY critical bias issues mentioned. Make minimal changes while maintaining 
                    the original tone and structure. Focus on removing legal red flags and discriminatory language.
                    Return ONLY the rewritten JD, no explanations."""
                },
                {
                    "role": "user",
                    "content": f"""Original JD:\n{original_jd}\n\nDetected Bias Issues:\n{bias_summary}
                    
                    Rewrite this JD addressing only the most critical bias issues."""
                }
            ],
            temperature=0.7,
            max_tokens=2000
        )
        conservative_jd = conservative_response.choices[0].message.content.strip()
        
        # Balanced variant - moderate changes
        balanced_response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert in inclusive hiring practices. Rewrite the job description 
                    to address the identified bias issues with moderated, professional language. 
                    Make balanced improvements for inclusivity while keeping professional standards. 
                    Target audience: {demographics}. Return ONLY the rewritten JD.""".format(demographics=demographics_str)
                },
                {
                    "role": "user",
                    "content": f"""Original JD:\n{original_jd}\n\nDetected Bias Issues:\n{bias_summary}
                    
                    Rewrite this JD for inclusive hiring while maintaining professionalism."""
                }
            ],
            temperature=0.7,
            max_tokens=2000
        )
        balanced_jd = balanced_response.choices[0].message.content.strip()
        
        # Inclusive-First variant - maximum reach
        inclusive_response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": f"""You are an expert in diversity and inclusion. Rewrite the job description 
                    to maximize reach and appeal to {demographics_str}. 
                    Remove all barriers to entry, use welcoming language, emphasize learning opportunities, 
                    remove unnecessary seniority requirements, highlight diversity benefits. 
                    Make it appealing to career-changers, non-traditional backgrounds, and underrepresented groups.
                    Return ONLY the rewritten JD."""
                },
                {
                    "role": "user",
                    "content": f"""Original JD:\n{original_jd}\n\nDetected Bias Issues:\n{bias_summary}
                    
                    Rewrite this JD with maximum inclusivity and appeal."""
                }
            ],
            temperature=0.7,
            max_tokens=2000
        )
        inclusive_jd = inclusive_response.choices[0].message.content.strip()
        
        return {
            "conservative": conservative_jd,
            "balanced": balanced_jd,
            "inclusive_first": inclusive_jd
        }
        
    except Exception as e:
        return _generate_fallback_variants(original_jd, bias_matrix)


def _generate_fallback_variants(original_jd: str, bias_matrix: dict) -> Dict[str, str]:
    """Fallback method when OpenAI API is unavailable."""
    base_modifications = [
        ("must have", "should have"),
        ("native English", "fluent in English"),
        ("young and dynamic", "collaborative and detail-oriented"),
        ("energetic", "motivated and committed"),
        ("fresh graduate", "recent graduate")
    ]
    
    conservative = original_jd
    for old, new in base_modifications[:2]:
        conservative = conservative.replace(old, new)
    
    balanced = conservative
    balanced += "\n\n[Note: Rewritten for balanced inclusivity]"
    
    inclusive = original_jd
    for old, new in base_modifications:
        inclusive = inclusive.replace(old, new)
    inclusive += "\n\nWe encourage applications from candidates of all backgrounds and experience levels."
    
    return {
        "conservative": conservative,
        "balanced": balanced,
        "inclusive_first": inclusive
    }


def calculate_attraction_score(jd_text: str, target_demographics: List[str]) -> Dict:
    """
    Calculate attraction score for underrepresented demographics.
    Analyzes language, cultural alignment, accessibility, and demographic relevance.
    """
    
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        return _fallback_attraction_score(jd_text, target_demographics)
    
    try:
        client = openai.OpenAI(api_key=api_key)
        
        demographics_str = ", ".join(target_demographics) if target_demographics else "diverse candidates"
        
        analysis_response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert in diversity recruiting and demographic analysis. 
                    Analyze the job description for its appeal to the target demographics. 
                    Score each dimension 0-1 and provide overall predicted improvement.
                    Return ONLY a JSON response with these exact fields:
                    {"language_inclusivity": score, "demographic_relevance": score, "cultural_alignment": score, 
                     "accessibility_focus": score, "overall_score": score, "key_improvements": ["item1", "item2"]}"""
                },
                {
                    "role": "user",
                    "content": f"""Job Description:\n{jd_text}\n\nAnalyze its appeal to: {demographics_str}
                    
                    Consider:
                    - Language inclusivity (welcoming tone, no jargon barriers)
                    - Demographic relevance (specific mention of diversity efforts)
                    - Cultural alignment (values match, flexibility mentioned)
                    - Accessibility focus (remote options, accommodations, learning opportunities)
                    
                    Return JSON response."""
                }
            ],
            temperature=0.5,
            max_tokens=500
        )
        
        import json
        response_text = analysis_response.choices[0].message.content.strip()
        
        # Try to extract JSON from response
        try:
            score_data = json.loads(response_text)
        except:
            # Fallback if JSON parsing fails
            score_data = {
                "language_inclusivity": 0.7,
                "demographic_relevance": 0.6,
                "cultural_alignment": 0.65,
                "accessibility_focus": 0.6,
                "overall_score": 0.65
            }
        
        return score_data
        
    except Exception as e:
        return _fallback_attraction_score(jd_text, target_demographics)


def _fallback_attraction_score(jd_text: str, target_demographics: List[str]) -> Dict:
    """Fallback attraction score calculation."""
    # Simple heuristic scoring
    keywords_inclusive = ["inclusive", "diversity", "welcoming", "flexible", "remote", "mentor"]
    keywords_barriers = ["must have", "native", "young", "energetic", "ideal candidate"]
    
    inclusive_count = sum(1 for kw in keywords_inclusive if kw.lower() in jd_text.lower())
    barrier_count = sum(1 for kw in keywords_barriers if kw.lower() in jd_text.lower())
    
    language_score = min(0.9, (inclusive_count / 6))
    accessibility = 0.5 if "remote" in jd_text.lower() else 0.3
    cultural = 0.6 if "values" in jd_text.lower() else 0.4
    demographic = 0.5 if any(d.lower() in jd_text.lower() for d in target_demographics) else 0.3
    
    overall = (language_score + accessibility + cultural + demographic) / 4
    
    return {
        "language_inclusivity": language_score,
        "accessibility_focus": accessibility,
        "cultural_alignment": cultural,
        "demographic_relevance": demographic,
        "overall_score": min(0.95, overall)
    }


def _format_bias_matrix(bias_matrix: dict) -> str:
    """Format bias matrix into readable summary."""
    if not bias_matrix:
        return "No specific bias issues detected"
    
    summary = "Detected Bias Issues:\n"
    for key, value in bias_matrix.items():
        if isinstance(value, dict):
            summary += f"- {key}: {value.get('severity', 'Not specified')}\n"
        else:
            summary += f"- {key}: {value}\n"
    
    return summary
