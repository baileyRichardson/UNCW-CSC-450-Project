import requests
from flask import *

import Database
import DatabaseUse
import Notifications
import Playtime
import steamSetting
import userManger
import accountSettings
from Report import Report, ReportException
from SteamUser import SteamUser
import pyrebase
from flask import json
import os
from werkzeug.exceptions import HTTPException
from pysteamsignin.steamsignin import SteamSignIn
import DatabaseTest


app = Flask(__name__)
key = os.urandom(12).hex()
app.secret_key = key
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
            user = authentication.sign_in_with_email_and_password(email, password)
            user = authentication.refresh(user['refreshToken'])
            user_token = user["idToken"]
            session["user"] = user_token
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
    try:
        print(session["user"])
        username = "John Smith"
        # DatabaseTest.test("test@gmail", 12345)
        return render_template("dashboard.html", user=username)
    except KeyError:
        return render_template("loginPage.html")


@app.route('/reports/')
def reports():
    try:
        print(session["user"])
        user_id = "10000"
        user_report = Report(user_id)
        user_report_data = user_report.get_report(reports_page=True)
        return render_template("reports.html", reportData=user_report_data, accountLinked=True)
    except KeyError:
        return render_template("loginPage.html")
    except ReportException:
        return render_template("reports.html", accountLinked=False)


@app.route('/settings/')
def settings():
    try:
        print(session["user"])
        return render_template("settings.html")
    except KeyError:
        return render_template("loginPage.html")

    
@app.route('/processlogin/')
def process():
    try:
        print(session["user"])
        returnData = request.values

        steamLogin = SteamSignIn()
        steamID = steamLogin.ValidateResults(returnData)

        print('SteamID returned is: ', steamID)
        DatabaseUse.add_steam_account("test@gmail", steamID)

        if steamID is not False:
            return 'We logged in successfully!<br />SteamID: {0}<br />Click <a href="/settingSteamAccount"> to go back'.format(steamID)
        else:
            return 'Failed to log in, bad details?'
    except KeyError:
        return render_template("loginPage.html")


@app.route('/test/')
def test():
    try:
        print(session["user"])
        shouldLogin = request.args.get('test')
        print(shouldLogin)
        if shouldLogin is not None:
            steamLogin = SteamSignIn()
            return steamLogin.RedirectUser(steamLogin.ConstructURL('http://127.0.0.1:5000/processlogin'))
        return 'Click <a href="/test/?test=true">to log in</a>'
    except KeyError:
        return render_template("loginPage.html")


@app.route('/settingSteamAccount', methods=["GET", "POST"])
def settingSteamAccount():
    try:
        print(session["user"])
        accounts = Database.list_of_steam_accounts("test@gmail")
        limits = []
        for item in accounts:
            limits.append(Database.get_playtime_limit("test@gmail", item))
        if request.method == "POST":
            default_value = 'off'
            # iterate through steam accounts and get input data for each account
            for account in accounts:
                steam_account = request.form.get("steamAccount"+account, default_value)
                prev_limit = Database.get_playtime_limit("test@gmail", steam_account)
                auto = request.form.get("auto"+account, default_value)
                limit = request.form.get("limit"+account, "null")
                print("limit is"+limit+"with type:"+str(type(limit)))
                print(prev_limit)
                # remove steam account
                remove = request.form.get("confirmRemove"+account, default_value)
                DatabaseUse.update_steam_account_page("test@gmail", steam_account, auto, remove, limit)
            new_accounts = Database.list_of_steam_accounts("test@gmail")
            new_limits = []
            for item in new_accounts:
                new_limits.append(Database.get_playtime_limit("test@gmail", item))
            return render_template("settingSteamAccount.html", results=new_accounts, limits=new_limits)
        return render_template("settingSteamAccount.html", results=accounts, limits=limits)
    except KeyError:
        return render_template("loginPage.html")


@app.route("/settingNotifications", methods=["GET", "POST"])
def settingNotifications():
    try:
        print(session["user"])
        email = Database.get_email("test@gmail")
        notification = DatabaseUse.interpret_notification_time("test@gmail")
        if request.method == "POST":
            default_value = 2
            often = request.form.get("often", default_value)
            DatabaseUse.update_notifications_page("test@gmail", int(often))
            new_notification = DatabaseUse.interpret_notification_time("test@gmail")
            return render_template("settingNotifications.html", email=email, often=new_notification)
        return render_template("settingNotifications.html", email=email, often=notification)
    except KeyError:
        return render_template("loginPage.html")



@app.route("/settingPlaytimeTracking")
def settingPlaytimeTracking():

    try:
        print(session["user"])
        steamAccounts = Database.list_of_steam_accounts("test@gmail")
        nested = []
        for item in steamAccounts:
            nested.append(Database.list_of_tracked_games("test@gmail", item))
        print(nested)
        return render_template("settingPlaytimeTracking.html", steam=steamAccounts, nested=nested)
    except KeyError:
        return render_template("loginPage.html")



@app.route("/settingWatchList")
def settingWatchList():
    try:
        print(session["user"])
        steamAccounts = Database.list_of_steam_accounts("test@gmail")
        nested = []
        all_prices = []
        for item in steamAccounts:
            nested.append(Database.list_of_watched_games("test@gmail", item))
        print(nested)
        return render_template("settingWatchList.html", steam=steamAccounts, nested=nested)
    except KeyError:
        return render_template("loginPage.html")



@app.route('/forgotPass/', methods=["GET", "POST"])
def forgotPassword():
    if request.method == "POST":
        try:
            email = request.form["name"]
            authentication.send_password_reset_email(email)
            return render_template("loginPage.html")
        except requests.HTTPError as exception:
            error_json = exception.args[1]
            error = json.loads(error_json)["error"]["message"]
            if error == "INVALID_EMAIL":
                error_text = "We have no record of a Steam Monitor account using this email address."
            else:
                error_text = "Whoops, looks like we have an unaccounted for error: " + error
            return render_template("forgotPassword.html", errors=error_text)
    return render_template("forgotPassword.html")


@app.route('/signup/', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["name"]
        password = request.form["pass"]
        try:
            authentication.create_user_with_email_and_password(email, password)
            userManger.userManager(email)
            return render_template("loginPage.html")
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
