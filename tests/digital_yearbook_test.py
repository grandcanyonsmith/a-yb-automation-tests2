import pytest

from dotenv import load_dotenv
from os import environ as env
from selenium.webdriver import Chrome

load_dotenv()

@pytest.fixture(scope="session")
def browser():
    # Initialize ChromeDriver
    driver = Chrome()

    # Wait implicitly for elements to be ready before attempting interactions
    driver.implicitly_wait(10)

    # Return the driver object at the end of setup
    yield driver

    # For cleanup, quit the driver
    driver.quit()


def login_to_culture_cloud(browser, url, username, password):
    browser.get(url)

    username_field = browser.find_element('id', 'usernameField')

    username_field.send_keys(username)

    next_button = browser.find_element('id', "nextButton")
    next_button.click()

    password_field = browser.find_element('id', "passwordField")
    password_field.send_keys(password)

    sign_in_button = browser.find_element('id', "signInButton")
    sign_in_button.click()


def test_login_to_culture_cloud(browser):
    # token = get_internal_service_token()
    # file = 'ui_users.csv'
    # options = {
    #     'customer_id': env['CUSTOMER_UUID'],
    #     'partial': True,
    #     'env': 'QA'
    # }
    # core_dataload(token, file, options)
    # tod = datetime.datetime.now()
    # d = datetime.timedelta(days=5)
    # five_days_ago = (tod - d).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    # create_celebrations(env['PROGRAM_UUID'], five_days_ago)
    login_to_culture_cloud(browser, env['CULTURE_CLOUD_URL'], env["AUTOMATION_USERNAME"],
                           env['AUTOMATION_USER_PASSWORD'])
