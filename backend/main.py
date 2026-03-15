from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import os
import logging
from dotenv import load_dotenv
from supabase import create_client, Client
from jose import jwt, JWTError
from typing import Optional

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI(
    title="NexCore Studio API",
    description="Backend service for contact form handling and waitlist management.",
    version="1.0.0"
)

# Supabase Setup
SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") # Use service role for backend
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")

if not SUPABASE_URL or not SUPABASE_KEY:
    logger.error("Supabase environment variables are missing!")
    supabase: Optional[Client] = None
else:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# CORS Configuration
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL, "http://localhost:3001"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# JWT Verification Dependency
async def get_current_user(authorization: str = Header(...)):
    if not SUPABASE_JWT_SECRET:
        raise HTTPException(status_code=500, detail="JWT Secret not configured")
    
    try:
        token = authorization.replace("Bearer ", "")
        payload = jwt.decode(token, SUPABASE_JWT_SECRET, algorithms=["HS256"], audience="authenticated")
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return user_id
    except JWTError as e:
        logger.error(f"JWT Verification failed: {e}")
        raise HTTPException(status_code=401, detail="Could not validate credentials")

class ContactForm(BaseModel):
    name: str
    email: EmailStr
    message: str

class StatusResponse(BaseModel):
    status: str

@app.get("/health", response_model=StatusResponse)
async def health():
    return {"status": "ok"}

@app.post("/contact", response_model=StatusResponse)
async def contact(form: ContactForm):
    try:
        logger.info(f"Received contact request from {form.email}")
        print(f"[contact] From: {form.name} <{form.email}>")
        return {"status": "received"}
    except Exception as e:
        logger.error(f"Error processing contact form: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# --- Waitlist Endpoints ---

@app.post("/waitlist/join")
async def join_waitlist(user_id: str = Depends(get_current_user)):
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase not initialized")
    
    try:
        # Get user email from profiles
        user_res = supabase.table("profiles").select("email").eq("id", user_id).single().execute()
        if not user_res.data:
            raise HTTPException(status_code=404, detail="User profile not found")
        
        email = user_res.data["email"]

        # Check if already in waitlist
        check_res = supabase.table("waitlist").select("*").eq("user_id", user_id).execute()
        if check_res.data:
            return check_res.data[0]

        # Insert into waitlist
        insert_res = supabase.table("waitlist").insert({
            "user_id": user_id,
            "email": email
        }).execute()
        
        return insert_res.data[0]
    except Exception as e:
        logger.error(f"Error joining waitlist: {e}")
        raise HTTPException(status_code=500, detail="Failed to join waitlist")

@app.get("/waitlist/position/{user_id}")
async def get_position(user_id: str, current_user: str = Depends(get_current_user)):
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase not initialized")
    
    # Ensure users can only check their own position
    if user_id != current_user:
        raise HTTPException(status_code=403, detail="Forbidden")

    try:
        res = supabase.table("waitlist").select("position").eq("user_id", user_id).single().execute()
        if not res.data:
            raise HTTPException(status_code=404, detail="Not on waitlist")
        return res.data
    except Exception as e:
        logger.error(f"Error fetching position: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/waitlist/count")
async def get_waitlist_count():
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase not initialized")
    
    try:
        # head=True for exact count without returning rows
        res = supabase.table("waitlist").select("*", count="exact").execute()
        return {"count": res.count}
    except Exception as e:
        logger.error(f"Error fetching count: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
