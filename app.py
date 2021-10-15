from flask import *
import Notifications
import Playtime
import steamSetting
import userManger
import accountSettings
import Report
import pyrebase

app = Flask(__name__)

#Firebase Authentication setup
firebaseConfig = { "apiKey": "AIzaSyB7UiA-ZyjEO-wO-9ofk9BzPId9wRe_ENs",
                    "authDomain": "csc-450-group-5-project.firebaseapp.com",
                    "databaseURL": "https://csc-450-group-5-project-default-rtdb.firebaseio.com",
                    "projectId": "csc-450-group-5-project",
                    "storageBucket": "csc-450-group-5-project.appspot.com",
                    "messagingSenderId": "248907054984",
                    "appId": "1:248907054984:web:3e56f6fefbb0ea8d67c43d",
                    "measurementId": "G-97CZL0FRJF"}

firebase = pyrebase.initialize_app(firebaseConfig)
authentication = firebase.auth()

@app.route('/', methods = ["get", "post"])
def login():
    unsuccessful = 'Please check your credentials'
    successful = 'Login successful'
    if request.method == 'POST':
        email = request.form['name']
        password = request.form['pass']
        try:
            authentication.sign_in_with_email_and_password(email, password)
            return render_template("dashboard.html")
        except:
            return render_template('loginPage.html', us=unsuccessful)

    return render_template('loginPage.html')

#Testing, creating random account
#authentication.create_user_with_email_and_password("tdn5547@uncw.edu", "password")
#Testing, logging in


@app.route('/dashboard/')
def dashboard():
    username = "John Smith"
    return render_template("dashboard.html", user=username)

@app.route('/reports/')
def reports():
    return render_template("reports.html")


@app.route('/settings/')
def settings():
    return render_template("settings.html")

@app.route('/signup/', methods = ["get", "post"])
def signup():
    if request.method == 'POST':
        email = request.form['name']
        password = request.form['pass']
        try:
            authentication.create_user_with_email_and_password(email, password)
            return render_template("dashboard.html")
        except:
            return render_template('loginPage.html')
    return render_template("signupPage.html")


if __name__ == '__main__':
    app.run()
