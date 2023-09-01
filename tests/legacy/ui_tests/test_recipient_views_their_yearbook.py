import logging

import pytest
from config import Config
from playwright.sync_api import sync_playwright
from utils import browser, page

# Constants
LAST_NAME = "Diamond"
ACCESS_NUMBER = "02096503442860"
MAIN_URL = "https://awardselect.com/a/index.html"

# Selectors
SELECTORS = {
    "LAST_NAME_FIELD": "input#lastName",
    "ACCESS_FIELD": "input#accessNumber",
    "SIGNIN_BUTTON": "button[type='submit']",
    "COMPANY_LOGO": "img[alt='OSKO Logo']",
    "RECIPIENT_NAME": "text=Congrats, Red",
    "ORDER_BUTTON": "a[class='btn']",
    "AWARD_OPTIONS": "text=Please choose one award",
}

LOGGER = logging.getLogger(__name__)


def login_to_page(page):
    """Function to login to the page."""
    page.goto(MAIN_URL)
    page.fill(SELECTORS["LAST_NAME_FIELD"], LAST_NAME)
    page.fill(SELECTORS["ACCESS_FIELD"], ACCESS_NUMBER)
    page.click(SELECTORS["SIGNIN_BUTTON"])


def verify_yearbook(page):
    """Function to verify the yearbook."""
    assert page.wait_for_selector(SELECTORS["COMPANY_LOGO"])
    assert page.wait_for_selector(SELECTORS["RECIPIENT_NAME"])
    assert page.wait_for_selector(SELECTORS["ORDER_BUTTON"])
    page.click(SELECTORS["ORDER_BUTTON"])


def test_recipient_views_their_yearbook(page):
    """Test function to check if recipient can view their yearbook."""
    login_to_page(page)
    verify_yearbook(page)


if __name__ == "__main__":
    pytest.main(["-v", "-s", __file__])
