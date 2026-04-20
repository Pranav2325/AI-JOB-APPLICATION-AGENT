from pydantic import BaseModel #it is used to create schemas
from typing import Optional,List # give optional or none 

class Job(BaseModel):
    title: str
    company:str
    location:str
    salary: Optional[str]=None
    experience:Optional[str]=None
    description: Optional[str]=None
    skills:List[str]=[]
    posted_date:Optional[str]=None
    url:str
    source:str
    
    
'''
requests- HTTP requests
bs4- HTML parser 
selenium- Browser automation
webdriver-manager- automatically download chromedriver
pydantic -data modelling
'''
