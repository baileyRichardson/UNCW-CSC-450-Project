from flask import Flask
import Notifications
import Playtime
import steamSetting
import userManger
import accountSettings
import Report

app = Flask(__name__)

@app.route('/')
def hello_world():  # put application's code here
    #return hello()
    return '<h3>' + Notifications.hello() + '<h3><h3>' + Playtime.hello() + '<h3><h3>' + steamSetting.hello() +\
           '<h3><h3>' + userManger.hello() + '<h3><h3>' + accountSettings.hello() + '<h3>''<h3>' + Report.hello() + '<h3>'

# call hello method from all six here

if __name__ == '__main__':
    app.run()
