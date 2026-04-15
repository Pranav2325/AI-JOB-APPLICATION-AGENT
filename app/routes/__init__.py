from fastapi import APIRouter
from app.services.scraper import scrape_indeed_jobs

router=APIRouter()

@router.get("/scrape")
def scrape_jobs(job_title:str,location:str,max_jobs:int=10,country: str = "india"):
    jobs=scrape_indeed_jobs(job_title,location,max_jobs,country)
    
    return{
        "total_found":len(jobs),
        "country":country,
        "jobs":[job.dict() for job in jobs]
    }
