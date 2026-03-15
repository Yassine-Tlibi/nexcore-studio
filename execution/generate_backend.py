"""
Generates FastAPI backend files: main.py and requirements.txt
Usage: python execution/generate_backend.py --root .
"""

import os
import argparse

MAIN_PY = '''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:3000")],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ContactForm(BaseModel):
    name: str
    email: EmailStr
    message: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/contact")
async def contact(form: ContactForm):
    # Log to console — replace with aiosmtplib email send if SMTP is configured
    print(f"[contact] From: {form.name} <{form.email}>")
    print(f"[contact] Message: {form.message}")
    return {"status": "received"}
'''

REQUIREMENTS = """fastapi
uvicorn
pydantic[email]
python-dotenv
aiosmtplib
"""

ENV_EXAMPLE = """# Frontend
FRONTEND_URL=http://localhost:3000

# SMTP (optional, for real email sending)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your@email.com
SMTP_PASS=yourpassword
CONTACT_RECEIVER=your@email.com
"""

def generate(root: str):
    files = {
        "backend/main.py": MAIN_PY,
        "backend/requirements.txt": REQUIREMENTS,
        ".env.example": ENV_EXAMPLE,
    }
    for path, content in files.items():
        full = os.path.join(root, path)
        with open(full, "w") as f:
            f.write(content)
        print(f"  [wrote] {full}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    generate(args.root)
    print("[backend] Done.")