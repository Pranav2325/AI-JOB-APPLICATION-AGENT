from fastapi import FastAPI
from app.config import APP_NAME,APP_VERSION,DEBUG

app=FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    debug=DEBUG
)

@app.get("/")
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