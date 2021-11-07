#this file is for the actual email instance
# class Email:
#
#     def __init__(self, emailAddress):
#         self.emailAddress = emailAddress
#
#     userName: str = ""

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
    user_report_text = user_report.generate_report_text()

    email_body = """\
    <html>
        <body>
        """
    for account in user_report_text:
        email_body = email_body + "<p> Hello, " + "here is a report for the Steam accounts linked to " + email + "</p>\n"
        email_body = email_body + "<p> Steam account: " +  account[0] + "</p>" + "\n" + "<table>"
        email_body = email_body + "<tr><th>Game</th><th>Playtime</th></tr>" + "\n"
        for game in account[1]:
            email_body = email_body + "<tr><td>" + game + "</td>" + "<td>" + str(account[1][game][0]) + "</td>" + "</tr>" + "\n"
        email_body = email_body + "</table>" + """</body>
        </html>
        """

    html = email_body

    html_msg = MIMEText(html, "html")

    msg.attach(html_msg)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:

        smtp.login("noreplySteamMonitor@gmail.com", "UNCWcsc450")

        smtp.send_message(msg)

send_email("baileyr0826@gmail.com", 1)

