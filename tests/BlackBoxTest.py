from playwright.sync_api import sync_playwright


def main():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)  # needs to be firefox in class.
        page = browser.new_page()
        page.goto('http://127.0.0.1:5000/')  # ('http://127.0.0.1:5000/') <--login screen

        heading_title_selector = '//h1'
        print(page.query_selector(heading_title_selector))  # click on title and print

        # 1st user story (forgot pass)
        try:
            forgot_pass = page.query_selector('[href="/forgotPass/"]')  # go to forgot password page
            forgot_pass.click()  # tests quick spam against forgot password email being given
            user_input = page.query_selector('[type="email"]')  # forgot password user story #1 Here
            user_input.type("wre9366@uncw.edu")
            page.query_selector('[type="submit"]').click()
        except:
            print('Forgot password failed')  # Note: This one actually sometimes passes and sometimes fails? (Bug?)
            exit()

        # 2nd user story (I want to see report page)
        report = page.query_selector_all('[class="test"')
        for games in report:
            print(games.query_selector('.test').inner_text())

        page.wait_for_timeout(60000)  # this is in milliseconds

        browser.close()


if __name__ == '__main__':
    main()
