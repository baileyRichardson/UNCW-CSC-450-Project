#this file is for the actual email instance
# class Email:
#
#     def __init__(self, emailAddress):
#         self.emailAddress = emailAddress
#
#     userName: str = ""

import smtplib

with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()

    smtp.login("noreplySteamMonitor@gmail.com", "UNCWcsc450")

    subject = "This is a test"
    body = "Hey cool this actually works"

    msg = f'Subject: {subject}\n\n{body}'

    smtp.sendmail("noreplySteamMonitor", "baileyr0826@gmail.com", msg)




