import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os
from dotenv import load_dotenv

load_dotenv()

def get_email_config():
    """Get email configuration from environment variables."""
    email = os.getenv("EMAIL")
    app_password = os.getenv("APP_PASSWORD")
    # Support multiple recipients (comma-separated string)
    recipients_str = os.getenv("RECIPIENT_EMAIL", email)
    
    if not email or not app_password:
        raise ValueError("EMAIL and APP_PASSWORD environment variables must be set")
    
    # Clean and split into list
    recipients = [r.strip() for r in recipients_str.split(",") if r.strip()]
    
    return email, app_password, recipients

def send_email(newsletter_body, subject="সময় ও দেশ - দৈনিক সংবাদ সংক্ষেপ", logo_path=None):
    """Send newsletter via Gmail SMTP with inline logo to multiple recipients."""
    
    email, app_password, recipients = get_email_config()
    
    # Create message
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = email
    msg["To"] = ", ".join(recipients)
    
    # Attach body as HTML
    body_part = MIMEText(newsletter_body, "html", "utf-8")
    msg.attach(body_part)
    
    # Attach inline logo if provided
    if logo_path and os.path.exists(logo_path):
        try:
            with open(logo_path, 'rb') as f:
                img = MIMEImage(f.read())
                img.add_header('Content-ID', '<logo>')
                img.add_header('Content-Disposition', 'inline', filename="logo.png")
                msg.attach(img)
        except Exception as e:
            print(f"⚠️ Could not attach logo: {e}")
    
    try:
        # Connect to Gmail SMTP server
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(email, app_password)
            server.send_message(msg)
        
        print(f"✅ Email sent successfully to: {', '.join(recipients)}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False

if __name__ == "__main__":
    # Test email sending
    print("Testing email config for recipients...")
    _, _, recs = get_email_config()
    print(f"Configured recipients: {recs}")
