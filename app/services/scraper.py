import time ##time-related functions
from typing import List #used for type hints
from bs4 import BeautifulSoup #html parser
from selenium import webdriver #needed to control browser programatically
from selenium.webdriver.chrome.service import Service #helps properly start/stop driver
from selenium.webdriver.chrome.options import Options #configure headless mode,user-agent,anti-detection tricks
from webdriver_manager.chrome import ChromeDriverManager #automatically installs chromedriver
from app.models import Job


def create_driver()-> webdriver.Chrome: #returns a configured chrome driver
    chrome_options=Options() #create options object
    chrome_options.add_argument("--headless") #runs browser without ui
    chrome_options.add_argument("--no-sandbox") #disable sandboxing
    chrome_options.add_argument("--disable-dev-shm-usage")#fix shared meomeory usage 
    chrome_options.add_argument("--disable-gpu") #servers dont have graphics cards so chrome not try to using gpu rendering
    chrome_options.add_argument("--window-size=1920,1080")#set a fake screen size 
    chrome_options.add_argument("--disable-blink-features=AutomationControlled") #helps to avoid bot detection
    #disable extra detections
    chrome_options.add_experimental_option("excludeSwitches",["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension",False)
    chrome_options.add_argument( #make request like real user
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
    
    service=Service(ChromeDriverManager().install()) #install chromedriver 
    driver=webdriver.Chrome(service=service,options=chrome_options) #lauch browser
    
    driver.execute_script(
        "Object.defineProperty(navigator,'webdriver',{get:()=>undefined})"#to hide bots
    )
    return driver

def get_job_description(driver,job_url:str)-> str:
    try:
        driver.get(job_url)
        time.sleep(3)
        soup=BeautifulSoup(driver.page_source,"html.parser")
        
        selectors = [
            {"class": "styles_JDC__dang-inner-html__h0K4t"},
            {"class": "jobDescription"},
            {"class": "job-desc"},
            {"id": "job-desc"},
        ]
        
        for selector in selectors:
            elem=soup.find("div",selector)
            if elem:
                text=elem.get_text(strip=True,separator=" ")
                if len(text)>100:
                    return text
        with open("debug_page.html", "w", encoding="utf-8") as f: #saves full HTML if extraction fails 
            f.write(driver.page_source)
        print(" Saved debug_page.html - description selector not found")

        return ""
    except Exception as e :
        print(f"Could not fetch description: {e}")
    

def scrape_naukri_jobs(job_title:str,location:str, max_jobs:int=20,country: str = "india")->List[Job]:
    jobs=[]
    driver=None #intializae driver variable 
    
    try:
        print("Starting browser...")
        driver=create_driver()

    

        search_term=job_title.lower().replace(" ","-")
        location_term=location.lower().replace(" ","-")

        
        url = f"https://www.naukri.com/{search_term}-jobs-in-{location_term}"

        print(f"Navigating to: {url}")
        driver.get(url) #loads job page
        
        print("⏳ Waiting for page to fully load...")
        time.sleep(5) 
        
        
        soup=BeautifulSoup(driver.page_source,"html.parser")  #parse page HTML   
        job_cards=soup.find_all("div",class_="srp-jobtuple-wrapper")
        print(f"Found {len(job_cards)} job cards on page")
        
        for card in job_cards[:max_jobs]:
            try:
                
                title_elem=card.find("a",class_="title")
                title=title_elem.get_text(strip=True) if title_elem else "No title"
                job_url=title_elem["href"] if title_elem else url
                
                company_elem=card.find("a",class_="comp-name")
                company=company_elem.get_text(strip=True) if company_elem else "No company"
                
                location_elem=card.find("span",class_="locWdth")
                job_location=location_elem.get_text(strip=True) if location_elem else location
                
                salary_elem=card.find("span",class_="sal")
                salary=salary_elem.get_text(strip=True) if salary_elem else None
                
                exp_elem=card.find("span",class_="expwdth")
                experience=exp_elem.get_text(strip=True) if exp_elem else None
                
                desc_elem=card.find("span",class_="job-desc")
                snippet=desc_elem.get_text(strip=True) if desc_elem else ""
                
                skill_elems=card.find_all("li",class_="tag-li")
                skills=[s.get_text(strip=True) for s in skill_elems]
                
                date_elem=card.find("span",class_="job-post-day")
                posted_date=date_elem.get_text(strip=True) if date_elem else None

                
                print(f"Fetching full description for: {title}")
                
                full_description=get_job_description(driver,job_url)
                description=full_description if full_description else snippet

                job=Job(
                    title=title,
                    company=company,
                    location=job_location,
                    salary=salary,
                    experience=experience,
                    description=description,
                    skills=skills,
                    posted_date=posted_date,
                    url=job_url,
                    source="naukri"   
                )
                
                jobs.append(job)
                print(f"Scraped: {title} at {company} | Skills: {skills}")
            except Exception as e:
                print(f"Error parsing one card: {e}")
                continue
        
           
    except Exception as e:
        print(f"Request failed:{e}")
    finally: #close browser
        if driver:
            driver.quit()
            print("Browser closed")
    
    return jobs
        

    
    