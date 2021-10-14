from flask import Flask
import Notifications
import Playtime
import steamSetting
import userManger
import accountSettings
import Report
import pyrebase

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
#Testing, creating random account
#authentication.create_user_with_email_and_password("tdn5547@uncw.edu", "password")
#Testing, logging in
email = "tdn5547@uncw.edu"
password = input("Enter Pass:")
authentication.sign_in_with_email_and_password(email,password)

app = Flask(__name__)

@app.route('/')
def hello_world():  # put application's code here
    #return hello()
    return '<h3>' + Notifications.hello() + '<h3><h3>' + Playtime.hello() + '<h3><h3>' + steamSetting.hello() +\
           '<h3><h3>' + userManger.hello() + '<h3><h3>' + accountSettings.hello() + '<h3>''<h3>' + Report.hello() + '<h3>'

# call hello method from all six here

if __name__ == '__main__':
    app.run()
