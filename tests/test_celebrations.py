import pytest
import re

from playwright.sync_api import Page, expect

API_KEY = ''
URL = ''
USER = ''
PASS = ''


@pytest.mark.ui


def test_personal_notes(page: Page):

    page.goto(URL)
    page.locator('id=usernameField').fill(USER)
    page.locator('id=nextButton').click()
    page.locator('id=passwordField').fill(PASS)
    page.locator('id=signInButton').click()

    expect(page.get_by_text("Anniversaries")).to_be_visible()

    page.locator('data-testid=celebrationCard>>nth=0').click()
    expect(page.get_by_text("Write a personal note"))
    page.locator('id=mui-4').click()
    page.keyboard.press("Control+Shift+A")
    page.keyboard.press("Delete")
    page.locator('id=mui-4').type("Testing the personal note modal with text")
    page.locator('data-testid=modal-preview-button').click()
    page.locator('data-testid=modal-save-button').click()
    page.locator('data-testid=notes-modal-button-done').click()


def test_profile(page: Page):

    page.goto(URL)
    page.locator('id=usernameField').fill(USER)
    page.locator('id=nextButton').click()
    page.locator('id=passwordField').fill(PASS)
    page.locator('id=signInButton').click()

    expect(page.get_by_text("Anniversaries")).to_be_visible()

    page.locator('data-testid=current-user-name-header').click()
    page.locator('data-testid=profile-link').click()
    page.wait_for_selector('data-testid=profile-sidebar')
    expect(page.get_by_text("Reports to")).to_be_visible()


