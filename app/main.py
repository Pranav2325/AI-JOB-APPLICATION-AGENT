from fastapi import FastAPI #help to fetch data
from app.config import APP_NAME,APP_VERSION,DEBUG
from app.routes import router

app=FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    debug=DEBUG
)# fastapi uses to build auto-doc in /docs
app.include_router(router,prefix="/api")
@app.get("/")# its decorator takes fuction directly below it 
def root():
    return {
        "message":f"Welcome to {APP_NAME}",
        "version":APP_VERSION,
        "status":"running",
        "debug_mode":DEBUG
    }

@app.get("/health")
def health_check():
    return {"status":"healthy"}


'''
python -m venv venv - virtual enviroment
source venv/Scripts/activate -to activate venv file 
pip- package installer like npm
__init.py__- to flag that folder is importable
uvicorn app.main:app --reload  its is a web server like node and app.main is module path and app is name of app and --reload auto restart like nodemon 

requests - For making HTTP requests (like fetch() in JS)
BeautifulSoup4 -For reading and parsing HTML (like document.querySelector in JS)
selenium -For controlling a real browser when JS rendering is needed
websockets- two way connection
SSE(server sent events)- one way connection
use StreamingResponse which use yield to pause connection

'''