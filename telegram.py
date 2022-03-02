from bs4 import BeautifulSoup
import time


class TelegramParser:
    login_wait = 30
    loading_wait = 15
    interaction_wait = 15

    root_url = "https://web.telegram.org/"

    session_dir = "session/telegram/"
    save_session = True

    def __init__(self, driver):
        self.driver = driver

    def authenticate(self):
        # time.sleep(self.login_wait)
        input("Please login and press Enter:")

    def report_channels(self, channels):
        for channel in channels:
            print("Opening channel")

            self.driver.get(channel)
            time.sleep(self.loading_wait)

            view_in_web_btn = self.driver.find_element_by_class_name("tgme_action_web_button")
            view_in_web_btn.click()
            time.sleep(self.interaction_wait)