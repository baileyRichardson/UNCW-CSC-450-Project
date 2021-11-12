

import smtplib
from Report import Report
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(email : str, frequency : int):

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Steam Monitor Report for " + email
    msg["from"] = "noreplySteamMonitor@gmail.com"
    msg["to"] = email

    user_id = "10000"
    user_report = Report(user_id)
    user_report_text = user_report.get_report(reports_email=True)

    html = user_report_text

    html_msg = MIMEText(html, "html")

    msg.attach(html_msg)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:

            smtp.login("noreplySteamMonitor@gmail.com", "UNCWcsc450")

            smtp.send_message(msg)
    except smtplib.SMTPAuthenticationError as e:
        print("The smtp server login is incorrect. Double check the email and password.")

# send_email("baileyr0826@gmail.com", 1)