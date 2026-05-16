import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from icalendar import Calendar, Event
from datetime import datetime, timedelta

def send_interview_email(candidate_email, candidate_name, details):
    # --- CONFIGURATION ---
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    SENDER_EMAIL = "gouseimmugh@gmail.com" 
    SENDER_PASSWORD = "wdhl qfzm zopp bzsu" 

    # 1. Create the Email Container
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = candidate_email
    msg['Subject'] = "Interview Invitation & Calendar Invite"

    # 2. Create the HTML Body
    body = f"<h3>Hi {candidate_name},</h3><p>Please find the interview details and calendar invite attached.</p>"
    msg.attach(MIMEText(body, 'html'))

    # 3. CREATE THE CALENDAR EVENT (.ICS)
    cal = Calendar()
    event = Event()
    
    # Set the start time (Combine date and time from your 'details' dictionary)
    # Note: You may need to format your date/time strings to Python datetime objects
    start_time = datetime.strptime(f"{details['date']} {details['time']}", "%Y-%m-%d %I:%M %p")
    
    event.add('summary', 'PowerBI Interview with Nexus AI- Round-1')
    event.add('dtstart', start_time)
    event.add('dtend', start_time + timedelta(hours=1)) # Default 1 hour duration
    event.add('description', f"Interview with Nexus AI for the position.")
    event.add('location', details['link'])
    
    cal.add_component(event)

    # 4. ATTACH THE CALENDAR FILE TO THE EMAIL
    part = MIMEBase('text', 'calendar', method='REQUEST')
    part.set_payload(cal.to_ical())
    encoders.encode_base64(part)
    part.add_header('Content-Description', 'invitation.ics')
    part.add_header('Content-Disposition', 'attachment; filename="invite.ics"')
    msg.attach(part)

    # 5. SEND EMAIL
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False