from pydantic import BaseModel
from typing import Optional 

class Job(BaseModel):
    title: str
    company:str
    location:str
    salary: Optional[str]=None
    description: Optional[str]=None
    url:str
    source:str