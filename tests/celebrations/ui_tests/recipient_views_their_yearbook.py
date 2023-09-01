import json
import logging

import pytest
import requests
from config import Config
from playwright.sync_api import sync_playwright

# Constants
login_details = Config.get_section("login")
testrail_details = Config.get_section("testrail")
SELECTORS = {
    "username_field": "id=usernameField",
    "password_field": "id=passwordField",
    "next_button": "id=nextButton",
    "signin_button": "id=signInButton",
}

# Logger
logger = logging.getLogger(__name__)

# TestRail Status IDs
STATUS_PASSED = 1
STATUS_FAILED = 5


class LoginPage:
    """
    Class representing the login page. It contains methods to interact with the login page.

    :param page: The page object from playwright
    """

    def __init__(self, page):
        self._page = page

    def login_to_page(self):
        """
        Logs into the page by filling the username and password fields and clicking the next and sign in buttons.

        :return: None
        """
        self._page.goto(login_details["url"])
        self._fill_field_and_click_button(
            SELECTORS["username_field"],
            login_details["username"],
            SELECTORS["next_button"],
        )
        self._fill_field_and_click_button(
            SELECTORS["password_field"],
            login_details["password"],
            SELECTORS["signin_button"],
        )

    def _fill_field_and_click_button(self, fill_selector, fill_value, click_selector):
        """
        Fills a field specified by fill_selector with fill_value and clicks a button specified by click_selector.

        :param fill_selector: The selector of the field to fill
        :param fill_value: The value to fill the field with
        :param click_selector: The selector of the button to click
        :return: None
        """
        try:
            self._page.fill(fill_selector, fill_value)
            self._page.click(click_selector)
        except Exception as e:
            logger.error(
                f"Failed to fill {fill_selector} or click {click_selector}: {str(e)}"
            )
            raise


class AnniversaryPage:
    """
    Class representing the anniversary page. It contains methods to interact with the anniversary page.

    :param page: The page object from playwright
    """

    def __init__(self, page):
        self._page = page

    def validate_personal_notes(self):
        """
        Tests the personal notes functionality on the anniversary page.

        :return: "Success" if the test passes
        """
        self._page.click("text=Anniversaries")
        self._page.click('css=[data-testid="celebrationCard"]:nth-child(6)')
        self._page.click("text=personal note")
        self._page.click("id=mui-4")
        self._page.keyboard.press("Control+Shift+A")
        self._page.keyboard.press("Delete")
        self._page.fill("id=mui-4", "Test the personal note modal with text")
        self._page.click("data-testid=modal-preview-button")
        self._page.click("data-testid=modal-save-button")
        self._page.click("data-testid=notes-modal-button-done")
        return "Success"

    def validate_profile(self):
        """
        Tests the profile functionality on the anniversary page.

        :return: "Success" if the test passes
        """
        self._page.click("text=Anniversaries")
        self._page.click("data-testid=current-user-name-header")
        self._page.click("data-testid=profile-link")
        self._page.wait_for_selector("data-testid=profile-sidebar", state="visible")
        self._page.wait_for_selector("text=Reports to", state="visible")
        return "Success"


@pytest.fixture(scope="module")
def browser_page():
    """
    Pytest fixture that sets up and tears down a page for testing.

    :return: A new page object from playwright
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser.new_page()
        browser.close()


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown(browser_page):
    """
    Pytest fixture that sets up and tears down a login page for testing.

    :param browser_page: The page object from playwright
    :return: None
    """
    LoginPage(browser_page).login_to_page()
    yield
    browser_page.close()


def test_login(browser_page):
    """
    Test function that tests the login functionality.

    :param browser_page: The page object from playwright
    :return: None
    """
    LoginPage(browser_page).login_to_page()


def test_anniversary_page(browser_page):
    """
    Test function that tests the anniversary page functionality.

    :param browser_page: The page object from playwright
    :return: None
    """
    anniversary_page = AnniversaryPage(browser_page)
    assert anniversary_page.validate_personal_notes() == "Success"
    assert anniversary_page.validate_profile() == "Success"


def post_test_result(run_id, case_id, status_id, comment=None):
    """
    Function that uploads the test result to TestRail.

    :param run_id: The ID of the test run
    :param case_id: The ID of the test case
    :param status_id: The ID of the test status
    :param comment: A comment about the test result
    :return: None
    """
    headers = {"Content-Type": "application/json"}
    auth = (testrail_details["email"], testrail_details["password"])
    data = {"status_id": status_id, "comment": "did not work"}
    response = requests.post(
        f"{testrail_details['url']}/index.php?/api/v2/add_result_for_case/{run_id}/{case_id}",
        headers=headers,
        auth=auth,
        data=json.dumps(data),
    )
    response.raise_for_status()


def execute_test_and_upload_result():
    """
    Function that executes the test and uploads the result to TestRail.

    :return: None
    """
    try:
        pytest.main(["-v", "-s", __file__])
        post_test_result(
            run_id=testrail_details["run_id"],
            case_id=testrail_details["case_id"],
            status_id=STATUS_PASSED,
            comment="Test passed",
        )

    except Exception as e:
        post_test_result(
            run_id=testrail_details["run_id"],
            case_id=testrail_details["case_id"],
            status_id=STATUS_FAILED,
            comment=str(e),
        )
        print("failed")
