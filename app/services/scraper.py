import time
from typing import List
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from app.models import Job


def create_driver()-> webdriver.Chrome:
    chrome_options=Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches",["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension",False)
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
    
    service=Service(ChromeDriverManager().install())
    driver=webdriver.Chrome(service=service,options=chrome_options)
    
    driver.execute_script(
        "Object.defineProperty(navigator,'webdriver',{get:()=>undefined})"
    )
    return driver

INDEED_DOMAINS = {
    "us": "www.indeed.com",
    "india": "in.indeed.com",
    "uk": "uk.indeed.com",
    "australia": "au.indeed.com",
    "canada": "ca.indeed.com",
}
    

def scrape_indeed_jobs(job_title:str,location:str, max_jobs:int=20,country: str = "india")->List[Job]:
    jobs=[]
    driver=None
    
    try:
        print("Starting browser...")
        driver=create_driver()

    

        search_term=job_title.replace(" ","+")
        location_term=location.replace(" ","+")

        domain = INDEED_DOMAINS.get(country.lower(), "in.indeed.com")
        url = f"https://{domain}/jobs?q={search_term}&l={location_term}"

        print(f"Navigating to: {url}")
        driver.get(url)
        
        print("⏳ Waiting for page to fully load...")
        time.sleep(6)
        
        
        soup=BeautifulSoup(driver.page_source,"html.parser")      
        job_cards=soup.find_all("div",class_="job_seen_beacon")
        print(f"Found {len(job_cards)} job cards on page")
        
        for card in job_cards[:max_jobs]:
            try:
                title_elem=card.find("h2",class_="jobTitle")
                title=title_elem.get_text(strip=True) if title_elem else "No title"
                
                company_elem=card.find("span",attrs={"data-testid":"company-name"})
                company=company_elem.get_text(strip=True) if company_elem else "No company"
                
                location_elem=card.find("div",attrs={"data-testid":"text-location"})
                job_location=location_elem.get_text(strip=True) if location_elem else "No location"
                
                salary_elem=card.find("div",class_="salary-snippet-container")
                salary=salary_elem.get_text(strip=True) if salary_elem else None
                
                link_elem=card.find("a",class_="jcs-JobTitle")
                job_url=f"https://www.indeed.com{link_elem['href']}" if link_elem else url

                job=Job(
                    title=title,
                    company=company,
                    location=job_location,
                    salary=salary,
                    url=job_url,
                    source="indeed"   
                )
                
                jobs.append(job)
                print(f"Scraped: {title} at {company}")
            except Exception as e:
                print(f"Error parsing one card: {e}")
                continue
        
           
    except Exception as e:
        print(f"Request failed:{e}")
    finally:
        if driver:
            driver.quit()
            print("Browser closed")
    
    return jobs
        