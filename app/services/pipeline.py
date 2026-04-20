import json
from app.services.scraper import scrape_naukri_jobs
from app.services.ai_service import (
    match_job_to_resume,
    tailor_resume,
    generate_cover_letter
)

def make_event(status:str,message:str,data:dict=None)->str:
    payload={
        "status":status,
        "message":message,

    }
    if data:
        payload["data"]=data

    return f"data: {json.dumps(payload)}\n\n" #dumps- dict->string \n\n-> SSE msg terminator  

def run_job_pipeline(
    job_title:str,
    location:str,
    resume:str,
    applicant_name:str,
    max_jobs: int=10,
    match_threshold:int=60
):
    yield make_event(
        "started",
        f"Starting job search for '{job_title}' in {location}"
    )
    
    yield make_event("scraping","Scraping job listings...")
    
    jobs=scrape_naukri_jobs(job_title,location,max_jobs)
    
    if not jobs:
        yield make_event("error","No jobs found. Try different search terms")
        return
    
    yield make_event(
        "scraped",
        f"Found {len(jobs)} jobs. Starting AI analysis...",
        {"total_jobs":len(jobs)}
    )
    
    results=[]
    
    for index,job in enumerate(jobs):#enumerate -> to getting index and value 
        job_dict=job.dict() #job object into dict
        
        yield make_event(
            "analyzing",
            f"Analyzing job {index+1} of {len(jobs)}: {job.title} at {job.company}"
        )
        description=job.description or f"{job.title} position at {job.company}"
        
        print(f"🔎 Description preview: {description[:200]}")
        print(f"🤖 Sending to AI for matching...")
        
        match_result=match_job_to_resume(
            resume,
            description,
            job.title
        )
        print(f"🎯 Raw AI result: {match_result}")
        score=match_result.get("match_score",0)
        
        yield make_event(
            "analyzed",
            f"Match score: {score}%",
            {"job":job.title,"score":score}
        )
        
        if score<match_threshold:
            yield make_event(
                "skipped",
                f"Score {score}% below threshold {match_threshold}%. Skipping."
            )
            continue
        
        yield make_event(
            "tailoring",
            f"Good match! Tailoring resume for {job.title}..."
        )
        
        tailor_result=tailor_resume(resume,description,job.title)
        
        yield make_event(
            "cover_letter",
            f"Generating cover letter for {job.title}..."
        )
        
        cover_result=generate_cover_letter(
            resume,
            description,
            job.title,
            applicant_name
        )
        
        results.append({
            "job":job_dict,
            "match":match_result,
            "tailored_resume":tailor_result,
            "cover_letter":cover_result
        })
        
        yield make_event(
            "completed_job",
            f"Fully processed: {job.title} at {job.company}",
            {"processed":len(results)}
        )
    yield make_event(
        "done",
        f"Pipeline complete! Processed {len(results)} matching jobs.",
        {"total_results":len(results),"results":results}
    )
    
    