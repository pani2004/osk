from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ContactRequest(BaseModel):
    name: str
    email: str
    subject: str
    message: str

class ContactResponse(BaseModel):
    status: str
    message: str

@app.post("/api/contact", response_model=ContactResponse)
async def send_contact_email(request: ContactRequest):
    if not request.name or not request.email or not request.subject or not request.message:
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "message": "All fields are required."
        })
    
    try:
        sender_email = os.getenv("EMAIL_USER")
        sender_password = os.getenv("EMAIL_PASS")
        recipient_email = os.getenv("EMAIL_TO")
        
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"New Contact Form Submission: {request.subject}"
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg.add_header("Reply-To", request.email)
        
        html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f9fafb;">
            <div style="background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <h2 style="color: #2563eb; border-bottom: 2px solid #2563eb; padding-bottom: 10px;">New Contact Form Submission from OSK</h2>
                <div style="margin: 20px 0;">
                    <p style="margin: 10px 0;"><strong style="color: #333;">Name:</strong> {request.name}</p>
                    <p style="margin: 10px 0;"><strong style="color: #333;">Email:</strong> {request.email}</p>
                    <p style="margin: 10px 0;"><strong style="color: #333;">Subject:</strong> {request.subject}</p>
                </div>
                <div style="margin: 20px 0;">
                    <h3 style="color: #333;">Message:</h3>
                    <div style="background-color: #f3f4f6; padding: 15px; border-left: 4px solid #2563eb; border-radius: 5px;">
                        <p style="margin: 0; white-space: pre-wrap;">{request.message}</p>
                    </div>
                </div>
                <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #e5e7eb; color: #6b7280; font-size: 12px;">
                    <p>This email was sent from the OSK website contact form.</p>
                    <p>Reply directly to this email to respond to {request.name}.</p>
                </div>
            </div>
        </div>
        """
        
        mime_html = MIMEText(html, "html")
        msg.attach(mime_html)
        
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        
        return ContactResponse(
            status="success",
            message="Thank you for your message! We will get back to you soon."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "message": "Failed to send message. Please try again later."
        })

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)