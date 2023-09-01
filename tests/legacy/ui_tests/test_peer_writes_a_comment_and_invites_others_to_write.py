import sys
import os
import requests

import pytest
from playwright.sync_api import sync_playwright

from utils import browser, page

# Constants
COMMENT_FROM_PEER = "It has been such a pleasure working with you! Here's to many more years of laughter and progress!"
PEER_EMAIL = "yearbook.test@octanner.com"
RECIPIENT_NAME = "Fantastic Fran"
IMAGE_ATTACHED_TO_COMMENT_URL = "https://plus.unsplash.com/premium_photo-1661868744712-82629aa98f6d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2374&q=80"
PAGE_URL = "https://vision-qa.appreciatehub.com/ui/yearbook/comment/L2FwaS9wZWVyL2NvbW1lbnRzLzkwOWEwMmY2MDc0YWU2YjkwYjQ4ZTk4ZmZhZjVhMjMzMzUzNTBlZjc_Y29tbWVudGVyRW1haWw9dGVzdEBvY3Rhbm5lci5jb20?locale=en_US"
IMAGE_FILE_PATH = "temp_image.jpg"


# Selectors
SELECTORS = {
    "COMMENT": "#comment-comment",
    "COMMENTOR_NAME": "#comment-name",
    "IMAGE": "#comment-image-0",
    "SUBMIT": "#submit-comment",
    "INVITE": "#invite-others",
    "TEXTAREA": "textarea",
    "BUTTON": "button",
    "PREVIEW_IMAGE_BUTTON": "div.clearfix > button",
}


def go_to_page(page):
    """Navigate to URL"""
    page.goto(PAGE_URL)


def leave_comment(page):
    """Post a comment"""
    page.fill(SELECTORS["COMMENT"], COMMENT_FROM_PEER)
    page.fill(SELECTORS["COMMENTOR_NAME"], RECIPIENT_NAME)


def download_image(url, file_path):
    """Download image from url and save to file_path"""
    response = requests.get(url)
    with open(file_path, "wb") as file:
        file.write(response.content)


def delete_image(file_path):
    """Delete the local image file"""
    if os.path.exists(file_path):
        os.remove(file_path)


def add_image(page):
    """Attach image to comment"""
    download_image(IMAGE_ATTACHED_TO_COMMENT_URL, IMAGE_FILE_PATH)
    page.set_input_files(SELECTORS["IMAGE"], IMAGE_FILE_PATH)
    page.click(SELECTORS["PREVIEW_IMAGE_BUTTON"])
    delete_image(IMAGE_FILE_PATH)


def submit_comment(page):
    """Submit the comment"""
    page.click(SELECTORS["SUBMIT"])


def invite_others(page):
    """Invite others via email"""
    page.click(SELECTORS["INVITE"])
    page.fill(SELECTORS["TEXTAREA"], PEER_EMAIL)
    page.click(SELECTORS["BUTTON"])


def test_peer_writes_a_comment_and_invites_others(page):
    """Test comment and invitation"""
    go_to_page(page)
    leave_comment(page)
    add_image(page)
    submit_comment(page)
    invite_others(page)


if __name__ == "__main__":
    pytest.main(["-v", "-s", __file__])
