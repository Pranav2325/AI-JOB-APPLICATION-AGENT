import os #module to talk with os for reading env and path
from dotenv import load_dotenv

load_dotenv() # it helps to read your env file 

APP_NAME=os.getenv("APP_NAME","AI Job Agent") #getenv used to access env 
APP_VERSION=os.getenv("APP_VERSION","0.1.0")
DEBUG=os.getenv("DEBUG","False").lower()=="true"