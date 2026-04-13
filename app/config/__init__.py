import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME=os.getenv("APP_NAME","AI Job Agent")
APP_VERSION=os.getenv("APP_VERSION","0.1.0")
DEBUG=os.getenv("DEBUG","False").lower()=="true"