import argparse
import json
import os
import pickle
import sys
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

import telegram
import instagram
from storage import BrowserStorage

site_report = {
    "telegram": telegram.TelegramParser,
    "instagram": instagram.InstagramParser
}

sites = {
    "telegram": ["http://t.me/oplottv"],
    "instagram": ["https://www.instagram.com/dustumjr/", "https://www.instagram.com/marivedler/"]
}


def ensure_folders_exist(file_name):
    if not os.path.exists(os.path.dirname(file_name)):
        os.makedirs(os.path.dirname(file_name))


def try_load_cookies(reporter):
    login_success = False

    # load cookies if they exist
    cookie_file = reporter.session_dir + "cookies.pkl"
    local_storage_file = reporter.session_dir + "localStorage.pkl"
    session_storage_file = reporter.session_dir + "sessionStorage.pkl"

    if os.path.exists(cookie_file):  # there are some cookies
        print("Loading cookies...")
        print("Navigate to a dummy URL...")
        driver.get(reporter.root_url + "dummyurl")
        time.sleep(reporter.loading_wait)

        print("Add for the current website...")
        cookies = pickle.load(open(cookie_file, "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)

        print("Loading localStorage...")
        localStorage = BrowserStorage(driver, "localStorage")
        localStorageData = pickle.load(open(local_storage_file, "rb"))
        for key, value in localStorageData.items():
            localStorage.set(key, value)

        print("Loading sessionStorage...")
        sessionStorage = BrowserStorage(driver, "sessionStorage")
        sessionStorageData = pickle.load(open(session_storage_file, "rb"))
        for key, value in sessionStorageData.items():
            sessionStorage.set(key, value)
        login_success = True
    else:
        print("No cookies file")

    return login_success

def try_login(reporter):
    cookie_file = reporter.session_dir + "cookies.pkl"
    local_storage_file = reporter.session_dir + "localStorage.pkl"
    session_storage_file = reporter.session_dir + "sessionStorage.pkl"

    print("Logging in...")
    reporter.authenticate()
    time.sleep(reporter.loading_wait)

    if reporter.save_session:
        print("Saving logged in session in cookies...")
        ensure_folders_exist(cookie_file)
        pickle.dump(driver.get_cookies(), open(cookie_file, "wb"))
        pickle.dump(
            BrowserStorage(driver, "localStorage").items(),
            open(local_storage_file, "wb"),
        )
        pickle.dump(
            BrowserStorage(driver, "sessionStorage").items(),
            open(session_storage_file, "wb"),
        )


if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument("requested_site", choices=list(site_report.keys()))
    parse.add_argument("--relogin", required=False)

    args = parse.parse_args()

    # disable "Allow Notifications" pop-up
    options = ChromeOptions()
    options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(options=options)

    website_report = site_report[args.requested_site](driver)

    print("Navigating to the website...")
    driver.get(website_report.root_url)
    driver.implicitly_wait(website_report.loading_wait)
    time.sleep(website_report.loading_wait)

    if args.relogin or not try_load_cookies(website_report):
        try_login(website_report)
    else:
        print("Already logged in. Refreshing...")
        driver.get(website_report.root_url)
        time.sleep(website_report.loading_wait)

    # REPORT
    website_report.report_channels(sites[args.requested_site])

    driver.close()