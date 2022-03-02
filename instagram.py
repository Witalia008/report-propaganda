from bs4 import BeautifulSoup
import time


class InstagramParser:
    login_wait = 30
    loading_wait = 15
    interaction_wait = 3

    root_url = "https://www.instagram.com/"

    session_dir = "session/instagram/"
    save_session = True

    def __init__(self, driver):
        self.driver = driver

    def authenticate(self):
        input("Please login and press Enter:")
        # username_inp = self.driver.find_element_by_name("username")
        # username = input("Please enter phone number, username, or email: ")
        # for key in username:
        #     username_inp.send_keys(key)
        #     time.sleep(1)
        # time.sleep(self.interaction_wait)

        # password_inp = self.driver.find_element_by_name("password")
        # username = input("Please enter your password: ")
        # for key in username:
        #     username_inp.send_keys(key)
        #     time.sleep(1)
        # time.sleep(self.interaction_wait)

        # login_btn = self.driver.find_element_by_xpath("//button[@type='submit']")
        # login_btn.click()
        # time.sleep(self.interaction_wait)

        # time.sleep(self.login_wait)

    def report_channels(self, channels):
        for channel in channels:
            print("Opening channel")

            self.driver.get(channel)
            time.sleep(self.loading_wait)

            # Click ellipsis
            self.driver.find_element_by_class_name("wpO6b").click()
            time.sleep(self.interaction_wait)

            # Click "Report"
            self.driver.find_element_by_xpath("(//button[contains(concat(' ', normalize-space(@class), ' '), ' aOOlW ')])[3]").click()
            time.sleep(self.interaction_wait)


            # Click "Report Account"
            # Click “It’s posting content that shouldn’t be on Instagram”
            # Click “Violence or dangerous organisations”
            for btn_no in [2, 1, 7]:
                self.driver.find_element_by_xpath(f"(//div[@aria-label='Report']//button[contains(concat(' ', normalize-space(@class), ' '), ' b5k4S ')])[{btn_no}]").click()
                time.sleep(self.interaction_wait)

            # Click “Violent threat”
            self.driver.find_element_by_xpath("(//div[@aria-label='Report']//fieldset/div)[1]").click()
            time.sleep(self.interaction_wait)

            # Click “Submit report” button
            self.driver.find_element_by_xpath("(//div[@aria-label='Report']//button[contains(concat(' ', normalize-space(@class), ' '), ' sqdOP ')])").click()
            time.sleep(self.interaction_wait)