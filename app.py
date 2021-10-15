from flask import Flask, render_template
import DatabaseTest

app = Flask(__name__)


@app.route('/')
def dashboard():
    username = "000000002"
    steamName = 2
    return render_template("dashboard.html", user=DatabaseTest.test(username, steamName))


@app.route('/reports/')
def reports():
    return render_template("reports.html")


@app.route('/settings/')
def settings():
    return render_template("settingSteamAccount.html")


@app.route('/settings/steam_account')
def settingSteamAccount():
    return render_template("settingSteamAccount.html")

@app.route('/settings/playtime_tracking')
def settingPlaytimeTracking():
    return render_template("settingPlaytimeTracking.html")


@app.route('/settings/notifications')
def settingNotifications():
    return render_template("settingNotifications.html")


@app.route('/settings/watch_list')
def settingWatchList():
    return render_template("settingWatchList.html")

if __name__ == '__main__':
    app.run()
