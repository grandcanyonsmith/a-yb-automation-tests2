import pytest
from playwright.sync_api import sync_playwright

from utils import browser, page

# Constants
INCORRECT_EMAIL = "arialle.day@octanner.com"
CORRECT_EMAILS = ["arialle.dye@octanner.com", "Canyon.smith@octanner.com"]
MAIN_URL = "https://vision-qa.appreciatehub.com/ui/yearbook/comment/invites/L2FwaS9wZWVyL2xlYWRlci9pbnZpdGVzLzU2NmRkMGIyNjUyM2U0MWUyOWRiNGE1Mzk2ZTA1YjRhOGFmMGM4NjU?locale=en_US"

# Selectors
SELECTORS = {
    "TEXTAREA": "textarea",
    "LINK": ".invite-whom",
    "SEND_INVITE_BUTTON": "button:has-text('Send Invite')",
    "DONE_BUTTON": "button:has-text('Done')",
    "USER_CLOSE": ".user-close",
    "RESEND_INVITATION_BUTTON": "button:has-text('Resend Invitation')",
}


def go_to_page(page):
    """Navigate to main page"""
    page.goto(MAIN_URL)


def add_email(page, email):
    """Add email to textarea"""
    page.fill(SELECTORS["TEXTAREA"], email)
    page.press(SELECTORS["TEXTAREA"], "Enter")


def delete_email(page):
    """Delete the added email"""
    page.click(SELECTORS["USER_CLOSE"])
    assert not page.is_visible(
        f"text={INCORRECT_EMAIL}"
    )  # assert INCORRECT_EMAIL not visible


def handle_popup_modal(page):
    """Handle popup modal"""
    page.click(SELECTORS["LINK"])
    if page.is_visible(SELECTORS["DONE_BUTTON"]):
        page.click(SELECTORS["DONE_BUTTON"])


def add_correct_emails(page):
    """Add correct emails"""
    for email in CORRECT_EMAILS:
        add_email(page, email)
    for email in CORRECT_EMAILS:
        assert page.is_visible(f"text={email}")  # assert all correct emails are visible


def click_send_invite(page):
    """Click send invite button"""
    page.click(SELECTORS["SEND_INVITE_BUTTON"])
    if SELECTORS["RESEND_INVITATION_BUTTON"]:
        page.click(SELECTORS["RESEND_INVITATION_BUTTON"])
    assert page.wait_for_selector("text=Your invitations were sent!")


def test_manager_invites_others_to_write(page):
    """Test manager invite functionality"""
    go_to_page(page)
    add_email(page, INCORRECT_EMAIL)
    handle_popup_modal(page)
    delete_email(page)
    add_correct_emails(page)
    click_send_invite(page)


if __name__ == "__main__":
    pytest.main(["-v", "-s", __file__])
