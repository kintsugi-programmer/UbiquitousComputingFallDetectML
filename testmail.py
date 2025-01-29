import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

email_user = os.getenv('MAIL_USERNAME')
email_pass = os.getenv('MAIL_PASSWORD')
recipient = os.getenv('MAIL_RECIPIENT')

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()

try:
    server.login(email_user, email_pass)
    message = "Subject: Test Email\n\nThis is a test email from Flask."
    server.sendmail(email_user, recipient, message)
    print("Email sent successfully!")
except Exception as e:
    print(f"Email Sending Error: {str(e)}")
finally:
    server.quit()
