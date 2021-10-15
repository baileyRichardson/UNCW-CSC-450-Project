import requests
from flask import *
import Notifications
import Playtime
import steamSetting
import userManger
import accountSettings
import Report
import pyrebase
import DatabaseTest
from flask import json
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

# Firebase Authentication setup
firebaseConfig = {"apiKey": "AIzaSyB7UiA-ZyjEO-wO-9ofk9BzPId9wRe_ENs",
                  "authDomain": "csc-450-group-5-project.firebaseapp.com",
                  "databaseURL": "https://csc-450-group-5-project-default-rtdb.firebaseio.com",
                  "projectId": "csc-450-group-5-project",
                  "storageBucket": "csc-450-group-5-project.appspot.com",
                  "messagingSenderId": "248907054984",
                  "appId": "1:248907054984:web:3e56f6fefbb0ea8d67c43d",
                  "measurementId": "G-97CZL0FRJF"}

firebase = pyrebase.initialize_app(firebaseConfig)
authentication = firebase.auth()


@app.route('/', methods=["GET", "POST"])
def login():
    unsuccessful = "Please check your credentials"
    successful = "Login successful"
    if request.method == "POST":
        email = request.form["name"]
        password = request.form["pass"]
        try:
            authentication.sign_in_with_email_and_password(email, password)
            return render_template("dashboard.html")
        except requests.HTTPError as exception:
            error_json = exception.args[1]
            error = json.loads(error_json)["error"]["message"]
            if error == "EMAIL_NOT_FOUND":
                error_text = "No account linked to this email address can be found."
            else:
                error_text = "Whoops, looks like we have an unaccounted for error: " + error
            return render_template("loginPage.html", errors=error_text)

    return render_template("loginPage.html")


# Testing, creating random account
# authentication.create_user_with_email_and_password("tdn5547@uncw.edu", "password")
# Testing, logging in


@app.route('/dashboard/')
def dashboard():
    username = "000000002"
    steam = 12345
    return render_template("dashboard.html", user=DatabaseTest.test(username, 12345))


@app.route('/reports/')
def reports():
    return render_template("reports.html")


@app.route('/settings/')
def settings():
    return render_template("settings.html")


@app.route('/settings/settingSteamAccount')
def settingSteamAccount():
    return render_template("settingSteamAccount.html")

@app.route('/settings/settingPlaytimeTracking')
def settingPlaytimeTracking():
    return render_template("settingPlaytimeTracking.html")

@app.route('/settings/settingNotifications')
def settingNotifications():
    return render_template("settingNotifications.html")

@app.route('/settings/settingWatchList')
def settingWatchList():
    return render_template("settingWatchList.html")

@app.route('/signup/', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["name"]
        password = request.form["pass"]
        try:
            authentication.create_user_with_email_and_password(email, password)
            return render_template("dashboard.html")
        except requests.HTTPError as exception:
            error_json = exception.args[1]
            error = json.loads(error_json)["error"]["message"]
            if error == "EMAIL_EXISTS":
                return "This email is already in use."

    return render_template("signupPage.html")


if __name__ == '__main__':
    app.run()
