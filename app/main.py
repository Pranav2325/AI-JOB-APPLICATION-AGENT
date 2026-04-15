from fastapi import FastAPI
from app.config import APP_NAME,APP_VERSION,DEBUG
from app.routes import router

app=FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    debug=DEBUG
)
app.include_router(router,prefix="/api")
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