import os #module to talk with os for reading env and path
from dotenv import load_dotenv

load_dotenv() # it helps to read your env file 

APP_NAME=os.getenv("APP_NAME","AI Job Agent") #getenv used to access env 
APP_VERSION=os.getenv("APP_VERSION","0.1.0")
DEBUG=os.getenv("DEBUG","False").lower()=="true"
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY","")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

'''
openai- openai python library which handles api related fuctions
'''
