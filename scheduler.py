import os
import re
import smtplib
from datetime import datetime, timedelta
from email.message import EmailMessage
from urllib.parse import quote_plus, urlencode


TIME_SLOTS = [
    "09:00 AM",
    "10:00 AM",
    "11:30 AM",
    "01:30 PM",
    "03:00 PM",
    "04:30 PM",
]

INTERVIEW_MODES = [
    "Microsoft Teams",
    "Zoom",
    "Google Meet",
    "In-person",
]

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def is_valid_email(email):
    return bool(email and EMAIL_RE.match(email.strip()))


def parse_cc(cc_email):
    if not cc_email:
        return []
    values = [item.strip() for item in re.split(r"[,;]", cc_email) if item.strip()]
    return [item for item in values if is_valid_email(item)]


def default_subject(candidate_name, role):
    return f"Interview Invitation | {role} | {candidate_name}"


def default_body(candidate_name, role, date, time_slot, mode, link):
    return (
        f"Hi {candidate_name},\n\n"
        f"We are pleased to invite you to interview for the {role} role.\n\n"
        f"Interview details:\n"
        f"- Date: {date}\n"
        f"- Time: {time_slot}\n"
        f"- Mode: {mode}\n"
        f"- Link / Location: {link}\n\n"
        "A calendar invite is attached for your convenience. Please confirm your availability.\n\n"
        "Regards,\n"
        "Recruitment Team"
    )


def build_interview_payload(candidate, role, form_values):
    return {
        "name": candidate.get("Candidate", ""),
        "email": candidate.get("Email", ""),
        "date": str(form_values["date"]),
        "time": form_values["time"],
        "mode": form_values["mode"],
        "link": form_values["link"],
        "interviewer": form_values["interviewer"],
        "status": "Scheduled",
        "role": role,
        "notes": form_values.get("notes", ""),
        "subject": form_values.get("subject", ""),
        "body": form_values.get("body", ""),
        "from_email": form_values.get("from_email", ""),
        "cc_email": form_values.get("cc_email", ""),
    }


def combine_datetime(date_value, time_slot):
    return datetime.strptime(f"{date_value} {time_slot}", "%Y-%m-%d %I:%M %p")


def end_datetime(date_value, time_slot, minutes=60):
    return combine_datetime(date_value, time_slot) + timedelta(minutes=minutes)


def _ics_datetime(dt):
    return dt.strftime("%Y%m%dT%H%M%S")


def generate_ics(details):
    start = combine_datetime(details["date"], details["time"])
    end = start + timedelta(minutes=60)
    summary = details.get("subject") or default_subject(details.get("name", "Candidate"), details.get("role", "Interview"))
    description = (details.get("body") or "").replace("\n", "\\n")
    location = details.get("link", "")
    uid = f"{details.get('email', 'candidate')}-{_ics_datetime(start)}@synapse-ats"
    ics = "\r\n".join(
        [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//Synapse ATS//Interview Scheduler//EN",
            "CALSCALE:GREGORIAN",
            "METHOD:REQUEST",
            "BEGIN:VEVENT",
            f"UID:{uid}",
            f"DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}",
            f"DTSTART:{_ics_datetime(start)}",
            f"DTEND:{_ics_datetime(end)}",
            f"SUMMARY:{summary}",
            f"DESCRIPTION:{description}",
            f"LOCATION:{location}",
            f"ORGANIZER;CN={details.get('interviewer', 'Recruitment Team')}:MAILTO:{details.get('from_email', '')}",
            f"ATTENDEE;CN={details.get('name', 'Candidate')};RSVP=TRUE:MAILTO:{details.get('email', '')}",
            "END:VEVENT",
            "END:VCALENDAR",
            "",
        ]
    )
    return ics.encode("utf-8")


def google_calendar_url(details):
    start = combine_datetime(details["date"], details["time"])
    end = start + timedelta(minutes=60)
    params = {
        "action": "TEMPLATE",
        "text": details.get("subject") or default_subject(details.get("name", "Candidate"), details.get("role", "Interview")),
        "dates": f"{start.strftime('%Y%m%dT%H%M%S')}/{end.strftime('%Y%m%dT%H%M%S')}",
        "details": details.get("body", ""),
        "location": details.get("link", ""),
        "add": details.get("email", ""),
    }
    return "https://calendar.google.com/calendar/render?" + urlencode(params, quote_via=quote_plus)


def smtp_config():
    return {
        "host": os.getenv("SMTP_HOST", "smtp.gmail.com"),
        "port": int(os.getenv("SMTP_PORT", "587")),
        "username": os.getenv("SMTP_USERNAME", "gouseimmugh@gmail.com"),
        "password": os.getenv("SMTP_PASSWORD", "wdhl qfzm zopp bzsu"),
        "use_ssl": os.getenv("SMTP_USE_SSL", "false").lower() == "true",
    }


def validate_email_payload(details):
    errors = []
    if not is_valid_email(details.get("email", "")):
        errors.append("Candidate email is missing or invalid.")
    if not is_valid_email(details.get("from_email", "")):
        errors.append("From email is missing or invalid.")
    invalid_cc = [item for item in re.split(r"[,;]", details.get("cc_email", "")) if item.strip() and not is_valid_email(item.strip())]
    if invalid_cc:
        errors.append("One or more CC email addresses are invalid.")
    if not details.get("subject", "").strip():
        errors.append("Email subject is required.")
    if not details.get("body", "").strip():
        errors.append("Email body is required.")
    if not details.get("link", "").strip():
        errors.append("Meeting link or location is required.")
    return errors


def send_interview_email(details):
    validation_errors = validate_email_payload(details)
    if validation_errors:
        return False, " ".join(validation_errors)

    config = smtp_config()
    if not config["username"] or not config["password"]:
        return False, "SMTP credentials are not configured. For Gmail, use an app password."

    msg = EmailMessage()
    msg["Subject"] = details["subject"]
    msg["From"] = details["from_email"]
    msg["To"] = details["email"]
    cc_values = parse_cc(details.get("cc_email", ""))
    if cc_values:
        msg["Cc"] = ", ".join(cc_values)
    calendar_link = details.get("google_calendar_url", "")
    text_body = details["body"]
    html_body = details["body"].replace("\n", "<br>")
    if calendar_link:
        text_body += f"\n\nAdd to Google Calendar: {calendar_link}"
        html_body += f'<br><br><a href="{calendar_link}">Add to Google Calendar</a>'
    msg.set_content(text_body)
    msg.add_alternative(html_body, subtype="html")
    msg.add_attachment(
        generate_ics(details),
        maintype="text",
        subtype="calendar",
        filename="interview-invite.ics",
    )

    recipients = [details["email"]] + cc_values
    try:
        if config["use_ssl"]:
            with smtplib.SMTP_SSL(config["host"], config["port"], timeout=30) as server:
                server.login(config["username"], config["password"])
                server.send_message(msg, to_addrs=recipients)
        else:
            with smtplib.SMTP(config["host"], config["port"], timeout=30) as server:
                server.starttls()
                server.login(config["username"], config["password"])
                server.send_message(msg, to_addrs=recipients)
        return True, "Interview email sent with calendar attachment."
    except Exception as exc:
        return False, f"Email could not be sent: {exc}"
