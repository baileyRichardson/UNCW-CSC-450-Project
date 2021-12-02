

import smtplib
from Report import Report
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(user : str, email : str, frequency : int):

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Steam Monitor Report for " + email
    msg["from"] = "noreplySteamMonitor@gmail.com"
    msg["to"] = email

    #user_id = "10000"
    user_report = Report(user)
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


def send_limit_notification(limit, total, steam, email: str):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Playtime limit exceeded for " + email
    msg["from"] = "noreplySteamMonitor@gmail.com"
    msg["to"] = email

    html = (f'<!DOCTYPE html>\n'
            f'<html>\n'
            f'    <body>\n'
            f'        <p>The following is an email report:</p>\n'
            f'        <h1>The account {steam} has exceeded its playtime limit</h1>\n'
            f'        <h2>Limit: {limit} hours\n</h2>'
            f'        <h2>Hours played: {total} hours\n</h2>'
            f'    </body>\n'
            f'</html>')

    html_msg = MIMEText(html, "html")

    msg.attach(html_msg)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:

            smtp.login("noreplySteamMonitor@gmail.com", "UNCWcsc450")

            smtp.send_message(msg)
    except smtplib.SMTPAuthenticationError as e:
        print("The smtp server login is incorrect. Double check the email and password.")


