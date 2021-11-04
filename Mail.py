#this file is for the actual email instance
# class Email:
#
#     def __init__(self, emailAddress):
#         self.emailAddress = emailAddress
#
#     userName: str = ""

import smtplib
import time
from Report import Report
from email.message import EmailMessage

def send_email(email : str, frequency : int):
    user_id = "10000"
    user_report = Report(user_id)

    msg = EmailMessage()
    msg["Subject"] = "This is a test"
    msg["from"] = "noreplySteamMonitor@gmail.com"
    msg["to"] = email

    report_text = str(user_report.generate_report_text())


    print(report_text)
    msg.set_content(report_text)

    # with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    #
    #     smtp.login("noreplySteamMonitor@gmail.com", "UNCWcsc450")
    #
    #     smtp.send_message(msg)
    #     time.sleep(frequency * 60)

send_email("baileyr0826@gmail.com", 1)

