import pytest
"""
Author: Adan Narvaez Munguia
"""
from Report import Report, ReportException
from SteamUser import SteamUser


def test_instantiate_report():
    # "10000" corresponds to a test user. user_email is usually an email.
    user_id = "aan7056@uncwedu"
    # Instantiating a report object
    test_report = Report(user_id)
    # This specific test account should have a steam account in it.
    assert len(test_report.list_steam_accounts()) >= 1


def test_generate_report():
    # "10000" corresponds to a test user. user_email is usually an email.
    user_id = "aan7056@uncwedu"
    # Instantiating a report object
    test_report = Report(user_id)
    # Connecting to Steam and grabbing the random account.
    report_data: [SteamUser]
    report_data = test_report.get_report(reports_page=True)
    assert report_data[0].get_steam_name() is not None
