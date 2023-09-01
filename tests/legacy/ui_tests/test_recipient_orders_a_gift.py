import logging

import pytest
from playwright.sync_api import sync_playwright

from utils import browser, page

# Constants
LAST_NAME = "Appleseed"
ACCESS_NUMBER = "04670438787704"
URL = "https://acp.awardselect.com/60osko"

# Selectors
SELECTORS = {
    "LAST_NAME": "#lastName",
    "ACCESS_NUMBER": "#accessNumber",
    "ORDER_INST_LINK": "#order-inst a",
    "AWARD_LINK": "#award124 > a",
    "AWARDS_LIST_BUTTON": "div.awards-list button",
    "PLACE_ORDER_BUTTON": "#placeOrder",
    "CANCEL_LINK": "a.cancel",
    "YES_LINK": "a.yes",
    "LOGOUT_LINK": "#logoutFromNewHeader",
}


def login_to_awardselect(page):
    """Test for logging in to the website."""
    page.goto(URL)
    page.fill(SELECTORS["LAST_NAME"], LAST_NAME)
    page.fill(SELECTORS["ACCESS_NUMBER"], ACCESS_NUMBER)
    page.click("button")
    assert page.wait_for_selector(SELECTORS["LOGOUT_LINK"])


def test_navigate_to_order_instructions(page):
    """Test for navigating to order instructions."""
    page.click(SELECTORS["ORDER_INST_LINK"])


def select_award_and_add_to_cart(page):
    """Test for selecting an award and adding it to the cart."""
    page.click(SELECTORS["AWARD_LINK"])
    page.click(SELECTORS["AWARDS_LIST_BUTTON"])


def proceed_to_checkout(page):
    """Test for proceeding to checkout."""
    page.click("button")


def place_order(page):
    """Test for placing an order."""
    page.click(SELECTORS["PLACE_ORDER_BUTTON"])
    assert page.wait_for_selector("text='Order Complete'")


def cancel_order_and_logout(page):
    """Test for cancelling an order and logging out."""
    page.click(SELECTORS["CANCEL_LINK"])
    page.click(SELECTORS["YES_LINK"])
    page.click(SELECTORS["LOGOUT_LINK"])

def test_recipient_orders_a_gift(page):
    """Test for recipient ordering a gift."""
    login_to_awardselect(page)
    test_navigate_to_order_instructions(page)
    select_award_and_add_to_cart(page)
    proceed_to_checkout(page)
    place_order(page)
    cancel_order_and_logout(page)


if __name__ == "__main__":
    pytest.main(["-v", "-s", __file__])
