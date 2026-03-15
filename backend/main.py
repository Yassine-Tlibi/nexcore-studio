from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import os
import logging
from dotenv import load_dotenv

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI(
    title="NexCore Studio API",
    description="Backend service for contact form handling and health monitoring.",
    version="1.0.0"
)

# CORS Configuration
# Standardizing origins to include both development ports
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL, "http://localhost:3001"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ContactForm(BaseModel):
    name: str
    email: EmailStr
    message: str

class StatusResponse(BaseModel):
    status: str

@app.get("/health", response_model=StatusResponse)
async def health():
    """Returns the health status of the API."""
    return {"status": "ok"}

@app.post("/contact", response_model=StatusResponse)
async def contact(form: ContactForm):
    """
    Handles contact form submissions.
    Logs the submission to the logger.
    """
    try:
        logger.info(f"Received contact request from {form.email}")
        # In a production environment, this is where you would call aiosmtplib 
        # or an external service like SendGrid to send an actual email.
        print(f"[contact] From: {form.name} <{form.email}>")
        print(f"[contact] Message: {form.message}")
        return {"status": "received"}
    except Exception as e:
        logger.error(f"Error processing contact form: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
