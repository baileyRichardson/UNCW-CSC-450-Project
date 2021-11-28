import requests
import urllib3.exceptions
import werkzeug.exceptions
from flask import *

import Database
import DatabaseUse
# import Notifications
import Timer
from Playtime import Playtime
import userManager
import accountSettings
# import accountSettings
import tests.unit.databaseuse_test as DBT
from Report import Report, ReportException
from SteamUser import SteamUser
import pyrebase
from flask import json
import os
from werkzeug.exceptions import HTTPException
from pysteamsignin.steamsignin import SteamSignIn
import DatabaseTest
import steamStore
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import Mail

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

sched = BackgroundScheduler(daemon=True)
# will check for if a game is beneath a price
# sched.add_job(Timer.scheduler_update_database, 'interval', minutes=15)
# send out notifications
sched.add_job(Timer.scheduler_notification_day, 'cron', day_of_week='sat', hour=18, minute=34, misfire_grace_time=None)
sched.add_job(Timer.scheduler_notification_day, 'cron', hour=20, minute=22, misfire_grace_time=None)
sched.add_job(Timer.scheduler_notification_week, 'cron', day_of_week='sat', hour=15, misfire_grace_time=None)
# test lines
# sched.add_job(Timer.scheduler_notification_day, 'cron', day_of_week="*",hour="15", minute="45")
# sched.add_job(Timer.sc# timer_started = Falseheduler_notification_week, 'cron', day_of_week="*",hour="15", minute="45")
# turn off process when app is closed
atexit.register(lambda: sched.shutdown())


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
            Mail.send_email('tanareva123@gmailcom', 'tanareva123@gmail.com', 1)
            return render_template("dashboard.html")
        except requests.HTTPError as exception:
            error_json = exception.args[1]
            error = json.loads(error_json)["error"]["message"]
            if error == "EMAIL_NOT_FOUND":
                error_text = "Invalid login credentials. Please try again."
            elif error == "INVALID_PASSWORD":
                error_text = "Invalid login credentials. Please try again."
            elif error == "TOO_MANY_ATTEMPTS_TRY_LATER : Access to this account has been temporarily " \
                          "disabled due to many failed login attempts. You can immediately restore it " \
                          "by resetting your password or you can try again later.":
                error_text = "Your account has been temporarily disabled due to too many failed login" \
                             " attempts. Please reset your password or try again later."
            else:
                error_text = "Whoops, looks like we have an unaccounted for error: " + error
            return render_template("loginPage.html", errors=error_text)

    return render_template("loginPage.html")


@app.route('/dashboard/')
def dashboard():
    try:
        print(session["user"])
        return render_template("dashboard.html")
    except KeyError:
        return render_template("loginPage.html")


@app.route('/reports/')
def reports():
    try:
        print(session["user"])
        user_report = Report(
            authentication.get_account_info(session.get('user')).get('users')[0].get('email').replace(".", ""))
        # print("Steam Accounts are",user_report.steam_accounts[0].get_game_info())
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
        print(authentication.get_account_info(session.get('user')).get('users')[0].get('email').replace(".", ""))
        DatabaseUse.add_steam_account(
            authentication.get_account_info(session.get('user')).get('users')[0].get('email').replace(".", ""),
            int(steamID))

        if steamID is not False:
            return 'We logged in successfully!<br />SteamID: {0}<br />Click <a href="/dashboard"> to go back'.format(
                steamID)
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
        try:
            accounts = Database.list_of_steam_accounts(
                authentication.get_account_info(session.get('user')).get('users')[0].get('email').replace(".", ""))
            limits = []

            for item in accounts:
                limits.append(Database.get_playtime_limit(
                    authentication.get_account_info(session.get('user')).get('users')[0].get('email').replace(".", ""),
                    item))
            if request.method == "POST":
                default_value = 'off'
                # iterate through steam accounts and get input data for each account
                for account in accounts:
                    steam_account = request.form.get("steamAccount" + account, default_value)
                    prev_limit = Database.get_playtime_limit(
                        authentication.get_account_info(session.get('user')).get('users')[0].get('email').replace(".",
                                                                                                                  ""),
                        steam_account)
                    auto = request.form.get("auto" + account, default_value)
                    limit = request.form.get("limit" + account, "null")
                    print("limit is" + limit + "with type:" + str(type(limit)))
                    print(prev_limit)
                    # remove steam account
                    remove = request.form.get("confirmRemove" + account, default_value)
                    DatabaseUse.update_steam_account_page(
                        authentication.get_account_info(session.get('user')).get('users')[0].get('email').replace(".",
                                                                                                                  ""),
                        steam_account, auto, remove, limit)
                new_accounts = Database.list_of_steam_accounts(
                    authentication.get_account_info(session.get('user')).get('users')[0].get('email').replace(".", ""))
                new_limits = []
                for item in new_accounts:
                    new_limits.append(Database.get_playtime_limit(
                        authentication.get_account_info(session.get('user')).get('users')[0].get('email').replace(".",
                                                                                                                  ""),
                        item))
                return render_template("settingSteamAccount.html", results=new_accounts, limits=new_limits)
            return render_template("settingSteamAccount.html", results=accounts, limits=limits)
        except:
            return render_template("settingSteamAccount.html")

    except KeyError:
        return render_template("loginPage.html")


@app.route("/settingNotifications", methods=["GET", "POST"])
def settingNotifications():
    try:
        print(session["user"])
        try:
            email = authentication.get_account_info(session.get('user')).get('users')[0].get('email')
            notification = DatabaseUse.interpret_notification_time(
                authentication.get_account_info(session.get('user')).get('users')[0].get('email').replace(".", ""))
            if request.method == "POST":
                default_value = 2
                often = request.form.get("often", default_value)
                DatabaseUse.update_notifications_page(
                    authentication.get_account_info(session.get('user')).get('users')[0].get('email').replace(".", ""),
                    int(often))
                new_notification = DatabaseUse.interpret_notification_time(
                    authentication.get_account_info(session.get('user')).get('users')[0].get('email').reaplce(".", ""))
                return render_template("settingNotifications.html", email=email, often=new_notification)
            return render_template("settingNotifications.html", email=email, often=notification)
        except:
            notification = DatabaseUse.interpret_notification_time(
                authentication.get_account_info(session.get('user')).get('users')[0].get('email').replace(".", ""))
            return render_template("settingNotifications.html", email=email, often=notification)
    except KeyError:
        return render_template("loginPage.html")


@app.route("/settingPlaytimeTracking", methods=["GET", "POST"])
def settingPlaytimeTracking():
    try:
        print(session["user"])
        try:
            user_email = authentication.get_account_info(session.get('user')).get('users')[0].get('email').replace(".",
                                                                                                                   "")
            print(user_email)
            accounts = Report(user_email)
            account_list = accounts.get_report(reports_page=True)
            print(account_list)
            steamAccounts = []
            account: SteamUser
            for account in account_list:
                tracked_games = Database.list_of_tracked_games(user_email, account.get_steam_id())
                # print(tracked_games)
                steamAccounts.append((account.get_steam_name(), account.get_game_names(), tracked_games))
            print(steamAccounts)
            if request.method == "POST":
                for current_account in account_list:
                    new_game = request.form.get("game")
                    if new_game != "Select a game":
                        Database.add_tracked_game(new_game, user_email, current_account.get_steam_id())
                        tracked_games = Database.list_of_tracked_games(user_email, current_account.get_steam_id())
                        return render_template("settingPlaytimeTracking.html", steam=steamAccounts,
                                               tracked=tracked_games)
                    for game in tracked_games:
                        remove = request.form.get("confirmRemove" + game) or "off"
                        DatabaseUse.update_tracked_games_page(user_email, current_account.get_steam_id(), game, remove)
                        tracked_games = Database.list_of_tracked_games(user_email, current_account.get_steam_id())
                return render_template("settingPlaytimeTracking.html", steam=steamAccounts, tracked=tracked_games)
            return render_template("settingPlaytimeTracking.html", steam=steamAccounts, tracked=tracked_games)
        except:
            return render_template("settingPlaytimeTracking.html")
    except KeyError:
        return render_template("loginPage.html")


@app.route("/settingWatchList", methods=["GET", "POST"])
def settingWatchList():
    try:
        print(session["user"])
        # print(authentication.get_account_info(session.get('user')).get('users')[0].get('email').replace(".", ""))
        steamAccounts = Database.list_of_steam_accounts(
            authentication.get_account_info(session.get('user')).get('users')[0].get('email').replace(".", ""))
        # print('users')
        nested = []
        # print(steamAccounts)
        for item in steamAccounts:
            nested.append(Database.list_of_watched_games(
                authentication.get_account_info(session.get('user')).get('users')[0].get('email').replace(".", ""),
                item))
        add_result = ""
        update = ""
        if request.method == 'POST':
            watched_games = []
            for account in steamAccounts:
                watched_games.append(Database.list_of_watched_games(
                    authentication.get_account_info(session.get('user')).get('users')[0].get('email').replace(".", ""),
                    account))
                default_url = "1/2/3/4/5/"
                default_price = 00.00
                gameURL = request.form.get("game") or default_url
                price = float(request.form.get("price") or default_price)
                print(gameURL)
                print(price)
                add_result = DatabaseUse.add_to_watch_list(
                    authentication.get_account_info(session.get('user')).get('users')[0].get('email').replace(".", ""),
                    account, gameURL, price)
                for a in nested:
                    for b in a:
                        default_remove = "off"
                        remove = request.form.get("confirmRemove" + str(b) + b[0])
                        new_price = request.form.get("newPrice" + str(b) + b[0])
                        print(remove)
                        print(new_price)
                        update = DatabaseUse.update_watch_list_page(
                            authentication.get_account_info(session.get('user')).get('users')[0].get('email').replace(
                                ".", ""),
                            account, b[0], new_price, remove)
                return render_template("settingWatchList.html", steam=steamAccounts, nested=nested, add=add_result,
                                       update=update)
            return render_template("settingWatchList.html", steam=steamAccounts, nested=nested, add=add_result,
                                   update=update)
        return render_template("settingWatchList.html", steam=steamAccounts, nested=nested, add=add_result,
                               update=update)
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
            userManager.userManager(email)
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
    sched.start()
    app.run()

