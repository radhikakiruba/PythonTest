import pytest
from dotenv import load_dotenv
from config import AppConfig
from pages.document_page import DocumentPage
from utils.allure_handler import AllureLoggerHandler
import logging
import allure

def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="local", help="env: local, staging, or prod")


@pytest.fixture(scope="session")
def app_config(request):
    env = request.config.getoption("--env")  # e.g., 'staging'
    load_dotenv(f"tests/conf/{env}.env")

    config = AppConfig.load()

    # Validation: Fail fast if any URL is missing
    if not config.base_url:
        raise ValueError("BASE_URL is missing in .env file!")

    return config


@pytest.fixture
def document_page(page, app_config):
    # Pass the config object into the Page Object
    return DocumentPage(page, app_config)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # We only care about failures during the actual test call
    if report.when == 'call' and report.failed:
        # 1. Check if 'page' was used in this specific test
        page = item.funcargs.get('page')

        # 2. Safety: Only screenshot if it's a UI test (page exists)
        # and the browser/page is still active
        if page and not page.is_closed():
            allure.attach(
                page.screenshot(full_page=True),
                name="ui_failure_screenshot",
                attachment_type=allure.attachment_type.PNG
            )

def pytest_configure(config):
    # Get the logger you defined in your framework
    logger = logging.getLogger()

    if not any(isinstance(h, AllureLoggerHandler) for h in logger.handlers):
        logger.addHandler(AllureLoggerHandler())