from groq import Groq
from app.config import GROQ_API_KEY, GROQ_MODEL
import json

client=Groq(api_key=GROQ_API_KEY)

def ask_ai(system_prompt:str,user_prompt:str)->str:
    response=client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role":"system","content":system_prompt},
            {"role":"user","content":user_prompt},
        ],
        temperature=0.3,
        max_tokens=1000
    )
    return response.choices[0].message.content

def clean_json_response(raw:str)->str:
    cleaned=raw.strip()
    
    if "```" in cleaned:
        parts=cleaned.split("```")
        for part in parts:
            part=part.strip()
            if part.startswith("json"):
                part=part[4:].strip()
            if part.startswith("{"):
                return part
    return cleaned
    

def match_job_to_resume(resume:str,job_description:str,job_title:str)->dict:
    system_prompt = """You are an expert technical recruiter with 10 years of experience.
    Your job is to analyze how well a candidate's resume matches a job description.
    You must respond ONLY with valid JSON — no extra text, no markdown, no explanation outside the JSON.
    """
    user_prompt=f"""
    Analyze this resume against this job description and return a JSON object.

    JOB TITLE: {job_title}

    JOB DESCRIPTION:
    {job_description}

    CANDIDATE RESUME:
    {resume}

    Return this exact JSON structure:
    {{
        "match_score": <number between 0 and 100>,
        "matched_skills": [<list of skills found in both resume and job>],
        "missing_skills": [<list of skills in job but NOT in resume>],
        "strengths": [<list of 3 strong points about this candidate for this role>],
        "recommendation": "<one sentence: should we apply or not and why>"
    }}
    """
    try:
        raw_response = ask_ai(system_prompt, user_prompt)
        
        cleaned=clean_json_response(raw_response)
        result = json.loads(cleaned)
        return result

    except json.JSONDecodeError:
        return {
            "match_score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "strengths": [],
            "recommendation": "Invalid JSON from AI",
            "raw_response": raw_response
        }

    except Exception as e:
        return {
            "match_score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "strengths": [],
            "recommendation": "API Error occurred",
            "error": str(e)
        }

def tailor_resume(resume: str,job_description:str,job_title:str)->dict:
    system_prompt="""You are an expert resume writer and career coach.
    Your job is to tailor a candidate's resume to match a specific job description.
    Rules you must follow:
    - Never add skills or experience the candidate does not have
    - Rephrase existing experience using keywords from the job description
    - Reorder bullet points to highlight most relevant experience first
    - Keep the same basic structure and length
    - Respond ONLY with valid JSON, no markdown, no code blocks.
    Start directly with { and end with }."""
    
    user_prompt=f"""
    JOB TITLE: {job_title}

    JOB DESCRIPTION:
    {job_description}

    ORIGINAL RESUME:
    {resume}

    Rewrite the resume to better match this job.
    Return ONLY this JSON structure:
    {{
        "tailored_resume": "the complete rewritten resume as a single string",
        "changes_made": ["change 1", "change 2", "change 3"],
        "keywords_added": ["keyword1", "keyword2"],
        "ats_score_estimate": <number 0-100 estimating ATS match after tailoring>
    }}"""
    
    try:
        raw_response=ask_ai(system_prompt,user_prompt)
        cleaned=clean_json_response(raw_response)
        result=json.loads(cleaned)
        return result
    except json.JSONDecodeError:
        return {
            "tailored_resume": resume,
            "changes_made": [],
            "keywords_added": [],
            "ats_score_estimate": 0,
            "error": "Could not parse AI response",
            "raw_response": raw_response
        }
    except Exception as e:
        return{
            "tailored_resume": resume,
            "changes_made": [],
            "keywords_added": [],
            "ats_score_estimate": 0,
            "error": str(e)
        }
    

'''
response- full api result
choices- list of possible answer take fist answer print text
'''
