from fastapi import APIRouter
from app.services.scraper import scrape_indeed_jobs
from app.services.ai_service import match_job_to_resume,tailor_resume,generate_cover_letter


router=APIRouter()

@router.get("/scrape")
def scrape_jobs(job_title:str,location:str,max_jobs:int=10,country: str = "india"):
    jobs=scrape_indeed_jobs(job_title,location,max_jobs,country)
    
    return{
        "total_found":len(jobs),
        "country":country,
        "jobs":[job.dict() for job in jobs]
    }

@router.post("/match") #data travels in req,body 
def match_job(payload:dict): #fastapi automatically reads req.body give like dict
    resume=payload.get("resume","")
    job_description=payload.get("job_description","")
    job_title=payload.get("job_title","Unknown Role")
    
    if not resume or not job_description:
        return {"error":"Both resume and job_description are required"}
    result=match_job_to_resume(resume,job_description,job_title)
    return{
        "job_title":job_title,
        "analysis":result
    }

@router.post("/tailor")
def tailor_resume_route(payload:dict):
    resume=payload.get("resume","")
    job_description=payload.get("job_description","")
    job_title=payload.get("job_title","Unknown Role")
    
    if not resume or not job_description:
        return {"error":"Both resume and job_description are required"}
    
    result=tailor_resume(resume,job_description,job_title)
    
    return {
        "job_title":job_title,
        "result":result
    }

@router.post("/cover-letter")
def cover_letter_route(payload:dict):
    
    resume=payload.get("resume","")
    job_description=payload.get("job_description","")
    job_title=payload.get("job_title","Unknown Role")
    applicant_name=payload.get("applicant_name","Applicant")
    
    if not resume or not job_description:
        return {"error":"Both resume and job_description are required"}
    
    result=generate_cover_letter(
        resume,
        job_description,
        job_title,
        applicant_name
    )
    
    return {
        "applicant_name":applicant_name,
        "job_title":job_title,
        "result":result
    }