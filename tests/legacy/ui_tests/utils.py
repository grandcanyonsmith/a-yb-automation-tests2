import pytest
from playwright.sync_api import sync_playwright
from config import Config

# TestRail Status IDs
STATUS_PASSED = 1
STATUS_FAILED = 5

# Constants
LOGIN_DETAILS = Config.get_section("login")
TESTRAIL_DETAILS = Config.get_section("testrail")


@pytest.fixture(scope="module")
def browser():
    """
    Fixture to initialize and close the browser.
    """
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True)
    yield browser
    browser.close()
    playwright.stop()


@pytest.fixture(scope="module")
def page(browser):
    """
    Fixture to create a new page context.
    """
    context = browser.new_context()
    yield context.new_page()


def post_test_result(
    run_id, case_id, status_id, comment="This test failed for case_id"
):
    client = APIClient("https://octanner.testrail.io")
    client.user = TESTRAIL_DETAILS["email"]
    client.password = TESTRAIL_DETAILS["password"]
    data = {"status_id": status_id, "comment": comment}
    response = client.send_post(f"add_result_for_case/{run_id}/{case_id}", data)
    print("Successfully uploaded report into Testrail")
    return response


def execute_test_and_upload_result():
    try:
        pytest.main(["-v", "-s", __file__])
        post_test_result(
            run_id=TESTRAIL_DETAILS["run_id"],
            case_id=TESTRAIL_DETAILS["case_id"],
            status_id=STATUS_PASSED,
            comment="Test passed successfully",
        )
    except Exception as e:
        post_test_result(
            run_id=TESTRAIL_DETAILS["run_id"],
            case_id=TESTRAIL_DETAILS["case_id"],
            status_id=STATUS_FAILED,
            comment=str(e),
        )

    return "Success"
