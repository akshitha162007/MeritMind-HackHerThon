import json
import os
from typing import Dict, List, Any
from openai import OpenAI

INDIAN_BIAS_TAXONOMY = {
    "gender": [
        "he should", "male candidate", "brotherhood",
        "manpower", "assertive", "dominant", "aggressive leader",
        "strong personality", "chairman", "salesman"
    ],
    "age": [
        "young", "energetic team", "fresher preferred",
        "recent graduate", "digital native", "youthful",
        "age no bar but prefer young"
    ],
    "caste": [
        "cultural fit", "good family background",
        "well-settled family", "community references preferred"
    ],
    "college_tier": [
        "IIT preferred", "NIT preferred", "premier institute",
        "tier-1 college", "top university only",
        "ivy league or equivalent"
    ],
    "regional_language": [
        "Hindi mandatory", "Hindi fluency required",
        "North Indian preferred", "must speak Hindi",
        "Hindi speaking candidates only"
    ],
    "socioeconomic": [
        "excellent communication", "well-spoken",
        "presentable personality", "good English accent",
        "convent educated preferred"
    ],
    "matrimonial": [
        "willing to relocate", "no family commitments",
        "available for transfers", "no bond to location"
    ],
    "disability": [
        "physically fit", "no health issues",
        "able-bodied", "full physical fitness required"
    ]
}

SYSTEM_PROMPT = """You are an expert in Indian corporate hiring discrimination.
You have deep knowledge of caste-based discrimination,
college tier hierarchy bias, regional and language bias,
gender and matrimonial bias specific to Indian hiring context.

Analyze the job description and detect bias across these axes:
gender, age, caste, college_tier, regional_language,
socioeconomic, matrimonial, disability

Also detect COMPOUND INTERSECTIONS where 2 or more axes
combine to create layered discrimination against a specific
demographic group.

For every bias found:
1. Quote the EXACT trigger phrase from the JD
2. Name the axis and any compound intersections
3. Explain which demographic is harmed
4. Give severity score 1-10
5. Suggest an inclusive rewrite of that phrase

Respond ONLY with valid JSON in this exact structure:
{
  "overall_bias_score": <float 0-10>,
  "bias_flags": [
    {
      "axis": "<primary axis>",
      "intersectional_axes": ["<axis1>", "<axis2>"],
      "trigger_phrase": "<exact phrase>",
      "severity": <1-10>,
      "harmed_demographic": "<who is harmed>",
      "explanation": "<why this is biased>",
      "suggested_rewrite": "<inclusive alternative>"
    }
  ],
  "matrix": [
    {
      "axis_row": "<axis>",
      "axis_col": "<axis>",
      "score": <float>,
      "trigger_phrase": "<phrase>"
    }
  ],
  "summary": "<2 sentence summary>"
}"""

def analyze_jd_bias(jd_text: str) -> Dict[str, Any]:
    """Analyze JD for bias using GPT-4 with fallback to keyword matching."""
    api_key = os.getenv("OPENAI_API_KEY")
    
    if api_key:
        try:
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"Analyze this job description for bias:\n\n{jd_text}"}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            result_text = response.choices[0].message.content.strip()
            result = json.loads(result_text)
            return result
        except Exception as e:
            print(f"GPT-4 call failed: {e}, falling back to keyword matching")
    
    return _keyword_fallback_analysis(jd_text)

def _keyword_fallback_analysis(jd_text: str) -> Dict[str, Any]:
    """Fallback keyword-based bias detection."""
    jd_lower = jd_text.lower()
    bias_flags = []
    matrix_entries = []
    
    for axis, keywords in INDIAN_BIAS_TAXONOMY.items():
        for keyword in keywords:
            if keyword.lower() in jd_lower:
                idx = jd_lower.find(keyword.lower())
                start = max(0, idx - 50)
                end = min(len(jd_text), idx + len(keyword) + 50)
                trigger_phrase = jd_text[start:end].strip()
                
                severity = min(10, 5 + len([k for k in keywords if k.lower() in jd_lower]))
                
                flag = {
                    "axis": axis,
                    "intersectional_axes": [axis],
                    "trigger_phrase": trigger_phrase[:100],
                    "severity": severity,
                    "harmed_demographic": _get_harmed_demographic(axis),
                    "explanation": _get_explanation(axis, keyword),
                    "suggested_rewrite": _get_rewrite_suggestion(axis, keyword)
                }
                bias_flags.append(flag)
                
                matrix_entries.append({
                    "axis_row": axis,
                    "axis_col": axis,
                    "score": severity / 10.0,
                    "trigger_phrase": trigger_phrase[:50]
                })
    
    overall_score = min(10.0, (len(bias_flags) * 1.5))
    
    return {
        "overall_bias_score": overall_score,
        "bias_flags": bias_flags,
        "matrix": matrix_entries,
        "summary": f"Detected {len(bias_flags)} bias indicators across {len(set(f['axis'] for f in bias_flags))} axes."
    }

def _get_harmed_demographic(axis: str) -> str:
    """Get description of harmed demographic for each axis."""
    demographics = {
        "gender": "Women and non-binary individuals",
        "age": "Older workers and recent graduates",
        "caste": "Lower caste and marginalized communities",
        "college_tier": "State college graduates and first-generation professionals",
        "regional_language": "South Indian and non-Hindi speaking candidates",
        "socioeconomic": "Working-class and underprivileged backgrounds",
        "matrimonial": "Married women and those with family commitments",
        "disability": "People with disabilities"
    }
    return demographics.get(axis, "Specific demographic groups")

def _get_explanation(axis: str, keyword: str) -> str:
    """Get explanation for why this is biased."""
    explanations = {
        "gender": f"'{keyword}' uses gendered language that excludes women and non-binary candidates",
        "age": f"'{keyword}' signals age preference, excluding older or younger workers",
        "caste": f"'{keyword}' is a caste signal that discriminates based on social background",
        "college_tier": f"'{keyword}' creates educational hierarchy bias against non-elite institutions",
        "regional_language": f"'{keyword}' excludes non-Hindi speakers and signals regional bias",
        "socioeconomic": f"'{keyword}' is a class proxy that excludes working-class candidates",
        "matrimonial": f"'{keyword}' targets women with family responsibilities",
        "disability": f"'{keyword}' excludes people with disabilities"
    }
    return explanations.get(axis, f"'{keyword}' contains bias")

def _get_rewrite_suggestion(axis: str, keyword: str) -> str:
    """Get inclusive rewrite suggestion."""
    suggestions = {
        "gender": "Use gender-neutral language like 'candidate', 'engineer', 'professional'",
        "age": "Focus on skills and experience, not age: 'with X years of experience'",
        "caste": "Remove cultural fit language; focus on skills and values alignment",
        "college_tier": "Replace with 'strong engineering background' or 'relevant degree'",
        "regional_language": "Specify only job-critical languages: 'English fluency required'",
        "socioeconomic": "Replace with specific skills: 'strong communication skills'",
        "matrimonial": "Use neutral language: 'flexibility for occasional travel as needed'",
        "disability": "Remove fitness requirements unless job-critical"
    }
    return suggestions.get(axis, "Use inclusive language")

def generate_rewrite(jd_text: str, bias_report: Dict[str, Any], variant: str = "balanced") -> Dict[str, Any]:
    """Generate rewritten JD with bias fixes."""
    api_key = os.getenv("OPENAI_API_KEY")
    
    severity_threshold = {
        "conservative": 8,
        "balanced": 5,
        "aggressive": 0
    }.get(variant, 5)
    
    flags_to_fix = [f for f in bias_report.get("bias_flags", []) if f["severity"] >= severity_threshold]
    
    if not flags_to_fix:
        return {
            "rewritten_jd": jd_text,
            "changes": [],
            "new_bias_score": bias_report.get("overall_bias_score", 0)
        }
    
    if api_key:
        try:
            client = OpenAI(api_key=api_key)
            
            flags_text = "\n".join([
                f"- {f['trigger_phrase']}: {f['suggested_rewrite']}"
                for f in flags_to_fix
            ])
            
            rewrite_prompt = f"""Rewrite this job description to be more inclusive.
Replace these biased phrases with inclusive alternatives:
{flags_text}

Variant: {variant}
- conservative: fix only critical bias (severity 8-10)
- balanced: fix all significant bias (severity 5+)
- aggressive: maximize inclusivity, fix all flags

Original JD:
{jd_text}

Return ONLY valid JSON:
{{
  "rewritten_jd": "<full rewritten JD>",
  "changes": [
    {{"original": "<phrase>", "replacement": "<new phrase>", "reason": "<why changed>"}}
  ]
}}"""
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert in writing inclusive job descriptions."},
                    {"role": "user", "content": rewrite_prompt}
                ],
                temperature=0.5,
                max_tokens=2000
            )
            
            result_text = response.choices[0].message.content.strip()
            result = json.loads(result_text)
            
            rewritten_jd = result.get("rewritten_jd", jd_text)
            changes = result.get("changes", [])
            
            new_bias_score = max(0, bias_report.get("overall_bias_score", 0) - len(changes) * 0.8)
            
            return {
                "rewritten_jd": rewritten_jd,
                "changes": changes,
                "new_bias_score": new_bias_score
            }
        except Exception as e:
            print(f"GPT-4 rewrite failed: {e}")
    
    return _keyword_fallback_rewrite(jd_text, flags_to_fix, bias_report)

def _keyword_fallback_rewrite(jd_text: str, flags: List[Dict], bias_report: Dict) -> Dict[str, Any]:
    """Fallback rewrite using simple replacements."""
    rewritten = jd_text
    changes = []
    
    replacements = {
        "he should": "the candidate should",
        "male candidate": "candidate",
        "brotherhood": "team",
        "manpower": "workforce",
        "assertive": "confident",
        "dominant": "leadership-oriented",
        "aggressive leader": "strong leader",
        "young": "experienced",
        "energetic team": "dynamic team",
        "fresher preferred": "entry-level welcome",
        "IIT preferred": "strong engineering background",
        "NIT preferred": "strong engineering background",
        "premier institute": "reputable institution",
        "Hindi mandatory": "strong communication skills",
        "Hindi fluency required": "English fluency required",
        "North Indian preferred": "all regions welcome",
        "excellent communication": "clear communication",
        "well-spoken": "articulate",
        "presentable personality": "professional demeanor",
        "good English accent": "clear English",
        "willing to relocate": "flexibility for occasional travel",
        "no family commitments": "availability as needed",
        "physically fit": "able to perform job duties",
        "no health issues": "able to perform job duties",
        "cultural fit": "values alignment"
    }
    
    for original, replacement in replacements.items():
        if original.lower() in rewritten.lower():
            idx = rewritten.lower().find(original.lower())
            if idx != -1:
                rewritten = rewritten[:idx] + replacement + rewritten[idx + len(original):]
                changes.append({
                    "original": original,
                    "replacement": replacement,
                    "reason": "Removed bias"
                })
    
    new_bias_score = max(0, bias_report.get("overall_bias_score", 0) - len(changes) * 0.8)
    
    return {
        "rewritten_jd": rewritten,
        "changes": changes,
        "new_bias_score": new_bias_score
    }
