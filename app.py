from flask import Flask, render_template
import Notifications
import Playtime
import steamSetting
import userManger
import accountSettings
import Report

app = Flask(__name__)


@app.route('/')
def dashboard():
    username = "John Smith"
    return render_template("dashboard.html", user=username)

@app.route('/reports/')
def reports():
    return render_template("reports.html")


@app.route('/settings/')
def settings():
    return render_template("settings.html")


if __name__ == '__main__':
    app.run()
