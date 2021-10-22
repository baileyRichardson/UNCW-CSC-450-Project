import requests
from flask import *
import Notifications
import Playtime
import steamSetting
import userManger
import accountSettings
import Report
import pyrebase
from flask import json

import DatabaseTest

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
            elif error == "INVALID_PASSWORD":
                error_text = "The password you have entered is incorrect."
            elif error == "TOO_MANY_ATTEMPTS_TRY_LATER : Access to this account has been temporarily " \
                          "disabled due to many failed login attempts. You can immediately restore it " \
                          "by resetting your password or you can try again later.":
                error_text = "Your account has been temporarily disabled due to too many failed login" \
                             " attempts. Please reset your password or try again later."
            else:
                error_text = "Whoops, looks like we have an unaccounted for error: " + error
            return render_template("loginPage.html", errors=error_text)

    return render_template("loginPage.html")


# Testing, creating random account
# authentication.create_user_with_email_and_password("tdn5547@uncw.edu", "password")
# Testing, logging in


@app.route('/dashboard/')
def dashboard():
    username = "John Smith"
    DatabaseTest.test("000000002",12345)
    return render_template("dashboard.html", user=username)


@app.route('/reports/')
def reports():
    return render_template("reports.html")


@app.route('/settings/')
def settings():
    return render_template("settings.html")


@app.route('/settingSteamAccount')
def settingSteamAccount():
    return render_template("settingSteamAccount.html")


@app.route("/settingNotifications")
def settingNotifications():
    return render_template("settingNotifications.html")


@app.route("/settingPlaytimeTracking")
def settingPlaytimeTracking():
    return render_template("settingPlaytimeTracking.html")


@app.route("/settingWatchList")
def settingWatchList():
    return render_template("settingWatchList.html")


@app.route('/forgotPass/', methods=["GET", "POST"])
def forgotPassword():
    if request.method == "POST":
        email = request.form["name"]
        authentication.send_password_reset_email(email)

    return render_template("forgotPassword.html")


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
                error_text = "An account is already tied to this email address."
            elif error == "WEAK_PASSWORD : Password should be at least 6 characters":
                error_text = "You have entered a weak password. Please choose a new password" \
                             " that is at least 6 characters long."
            else:
                error_text = "Whoops, looks like we have an unaccounted for error: " + error
            return render_template("signupPage.html", errors=error_text)

    return render_template("signupPage.html")


if __name__ == '__main__':
    app.run()
