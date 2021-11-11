"""This files provides the unit test for the authorization aspect of the site. - Tan Ngo
The test is functioning, but not with intended results at the time being"""

import pytest
import app

def test_authorize_dashboard_nologin():
    with pytest.raises(expected_exception=AttributeError):
        app.render_template("dashboard.html")

def test_authorize_reports_nologin():
    with pytest.raises(expected_exception=AttributeError):
        app.render_template("reports.html")

def test_authorize_settings_nologin():
    with pytest.raises(expected_exception=AttributeError):
        app.render_template("settings.html")

def test_authorize_settingsNotif_nologin():
    with pytest.raises(expected_exception=AttributeError):
        app.render_template("settingNotifications.html")

def test_authorize_settingsWatch_nologin():
    with pytest.raises(expected_exception=AttributeError):
        app.render_template("settingWatchList.html")

def test_authorize_settingsPlaytime_nologin():
    with pytest.raises(expected_exception=AttributeError):
        app.render_template("settingPlaytimeTracking.html")

def test_authorize_settingsSteam_nologin():
    with pytest.raises(expected_exception=AttributeError):
        app.render_template("settingSteamAccount.html")




