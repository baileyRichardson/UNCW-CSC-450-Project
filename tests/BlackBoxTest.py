"""
Author: William Ebright
"""
from playwright.sync_api import sync_playwright
import time


def BB_test_pass_reset(page):
    try:
        print("\nCurrently testing password reset")
        # page.goto('http://127.0.0.1:5000/')  # Must start at login screen
        page.goto('https://app-l47rwjgwkq-ue.a.run.app/')  # Must start at login screen (webapp)
        forgot_pass = page.query_selector('[href="/forgotPass/"]')
        forgot_pass.click()
        time.sleep(0.2)
        user_input = page.query_selector('[type="email"]')
        user_input.type("wre9366@uncw.edu")
        time.sleep(0.2)
        page.query_selector('[class="button"]').click()
    except:
        print('Forgot password failed')
        # exit()  # added if we want a failed test to result if total failure


def BB_test_login(page):
    try:
        print("\nCurrently testing login page")
        # page.goto('http://127.0.0.1:5000/')  # Must start at login screen (local)
        page.goto('https://app-l47rwjgwkq-ue.a.run.app/')  # Must start at login screen (webapp)
        user_email = page.query_selector('[type="email"]')
        user_email.type("wre9366@uncw.edu")  # "tanareva123@gmail.com" <-- for properly testing reports
        time.sleep(0.2)
        user_pass = page.query_selector('[type="password"]')
        user_pass.type("password")  # also just "password" <-- for properly testing reports
        time.sleep(0.2)
        page.query_selector('[class="button"]').click()
    except:
        print('Failed to login')


def BB_test_reports(page):
    try:
        print("\nCurrently testing reports page")
        # page.goto('http://127.0.0.1:5000/dashboard/')  # Must start at dashboard (local)
        page.goto('https://app-l47rwjgwkq-ue.a.run.app/dashboard/')  # Must start at dashboard (webapp)
        page.query_selector('[href="/reports/"]').click()
        time.sleep(0.2)
        report = page.query_selector_all('[class="test"]')  # checks if games are there
        for games in report:
            print(games.query_selector('.test').inner_text())  # Print out those games if they are
    except:
        print('No games on reports page (yet?)')


def BB_test_steam_link_notLogged(page):
    try:
        print("\nCurrently testing steam-linking")
        # page.goto('http://127.0.0.1:5000/dashboard/')  # Must start at dashboard (local)
        page.goto('https://app-l47rwjgwkq-ue.a.run.app/dashboard/')  # Must start at dashboard (webapp)
        page.hover('[href="#"]')
        time.sleep(0.2)
        page.query_selector('[href="/settingSteamAccount"]').click()
        time.sleep(0.2)
        page.query_selector('[href="test/?test=true"]').click()
        time.sleep(0.2)
        page.query_selector('[id="steamAccountName"]').click().type("SteamMonitor")
        time.sleep(0.2)
        page.query_selector('[id="steamPassword"]').click().type("St3@mM0n1t0r")
        page.query_selector('[id="imageLogin"]').click()  # if ALREADY logged in, will fail here for now.
    except:
        print('Unsuccessful steam linking')


def BB_test_steam_link_logged(page):
    try:
        print("\nCurrently testing steam-linking")
        # page.goto('http://127.0.0.1:5000/dashboard/')  # Must start at dashboard (local)
        page.goto('https://app-l47rwjgwkq-ue.a.run.app/dashboard/')  # Must start at dashboard (webapp)
        page.hover('[href="#"]')
        time.sleep(0.2)
        page.query_selector('[href="/settingSteamAccount"]').click()
        time.sleep(0.2)
        page.query_selector('[href="test/?test=true"]').click()
        time.sleep(0.2)
        page.query_selector('[id="imageLogin"]').click()  # if not ALREADY logged in, will fail here for now.
    except:
        print('Unsuccessful steam linking')


def BB_test_set_notification(page):  # somethings got a bug here
    try:
        print("\nCurrently testing notification settings")
        # page.goto('http://127.0.0.1:5000/dashboard/')  # Must start at dashboard (local)
        page.goto('https://app-l47rwjgwkq-ue.a.run.app/dashboard/')  # Must start at dashboard (webapp)
        page.hover('[href="#"]')
        page.query_selector('[href="/settingNotifications"]').click()
        page.query_selector('[name="often"]').click()  # ask about this in class?
        time.sleep(2)
        page.query_selector('[value="2"]').click()
        time.sleep(0.2)
        page.query_selector('[value="Submit changes"]').click()
    except:
        print('Unsuccessful Notification setting')


def BB_test_watched_games(page):
    try:
        print("\nCurrently testing adding watched games")
        # page.goto('http://127.0.0.1:5000/dashboard/')  # Must start at dashboard (local)
        page.goto('https://app-l47rwjgwkq-ue.a.run.app/dashboard/')  # Must start at dashboard (webapp)
        page.hover('[href="#"]')
        page.query_selector('[href="/settingWatchList"]').click()
        user_game = page.query_selector('[type="text"]').click()
        user_game.type("https://store.steampowered.com/app/1252330/DEATHLOOP/")
        time.sleep(2)
        page.query_selector('[type="number"]').click().type("50.00")
        time.sleep(0.2)
        page.query_selector('[type="submit"]').click()
    except:
        print('Unsuccessful adding watched game')


def BB_test_signup_page(page, email, password):
    try:
        print("\nCurrently testing signup page")
        # page.goto('http://127.0.0.1:5000/')  # Must start at login screen (local)
        page.goto('https://app-l47rwjgwkq-ue.a.run.app/')  # Must start at login screen (webapp)
        page.query_selector('[href="/signup/"]').click()
        time.sleep(0.2)
        user_input = page.query_selector('[type="email"]')
        user_input.type(email)
        time.sleep(0.2)
        user_pass = page.query_selector('[type="password"]')
        user_pass.type(password)
        time.sleep(0.2)
        page.query_selector('[type="submit"]').click()
        page.query_selector('[href="/signup/"]').click()  # Should fail here if account already existed
        # account_exists_message = '/p'
        # print(page.query_selector_all('/main'))  # click on title and print
    except:
        print('failed or account already exists!')


def main():
    # Testing all user stories marked as "Done" and can be BB tested + all login screen possibilities.
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)  # needs to be firefox in class.
        page = browser.new_page()
        # page.goto('http://127.0.0.1:5000/')  # <--login screen on local
        page.goto('https://app-l47rwjgwkq-ue.a.run.app/')  #  <--login screen on webapp

        heading_title_selector = '//h1'
        print(page.query_selector(heading_title_selector))  # click on title and print

        # 1st user story: I want to be able to sign up for an account; should pass (1)
        BB_test_signup_page(page, "someguy@gmail.com", "password")
        time.sleep(2)
        # 2nd user story:  I want to be able to sign up for an account (but already exists); should fail (2)
        BB_test_signup_page(page, "someguy@gmail.com", "password")
        time.sleep(2)
        # 3rd user story: I want to recover/change my lost password; should pass (3)
        BB_test_pass_reset(page)
        time.sleep(2)  # We wait 2 seconds because the website just can't handle the fast inputs.
        # 4th user story: I want to be able to log in to the application; should pass (4)
        BB_test_login(page)
        time.sleep(2)
        # 5th user story: I want to see reports page; should fail (5)
        BB_test_reports(page)
        time.sleep(2)
        # 6th user story: I want to link my steam account to the application; should "pass" if already logged to
        # steam (6)
        BB_test_steam_link_notLogged(page)
        time.sleep(2)
        # 6th user story: I want to link my steam account to the application; should "pass" if already logged to
        # steam (7)
        BB_test_steam_link_logged(page)
        time.sleep(2)
        # 5th user story: I want to see reports page (Again); should "pass" this time but not fully implemented (8)
        BB_test_reports(page)
        time.sleep(2)
        # 7th user story: As a steam user I want to navigate to the notification settings tab to create a reminder; (9)
        BB_test_set_notification(page)
        time.sleep(2)
        # 8th user story: As a steam user I want to be notified when a game goes below my watched amount (10)
        BB_test_watched_games(page)

        page.wait_for_timeout(60000)  # this is in milliseconds, total 60 seconds.

        browser.close()


if __name__ == '__main__':
    main()
