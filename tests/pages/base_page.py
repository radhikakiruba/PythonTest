from playwright.sync_api import Page, expect
from tests.utils.logger import get_logger

class BasePage:
    def __init__(self, page, config):
        self.page = page
        self.config = config  # Store the config object
        self.logger = get_logger(self.__class__.__name__)
        # Common elements like a Global Loader or Toast notifications
        self.toast_notification = page.locator(".toast-message")
        self.global_spinner = page.locator("#app-loading-spinner")

    def goto(self, path: str):
        self.page.goto(f"{self.config.base_url}/{path}")

    def assert_path(self, path: str):
        expect(self.page).to_have_url(f"{self.config.base_url}{path}")

    def navigate(self, url='/'):
        """Navigates to a specific URL and waits for the network to be idle."""
        target_url = f"{self.config.base_url}{url}"
        self.page.goto(target_url, wait_until="domcontentloaded")

    def click_element(self, selector: str):
        """Wait for element to be visible and click it."""
        self.page.wait_for_selector(selector)
        self.page.click(selector)

    def get_text(self, selector: str) -> str:
        """Helper to get text from a locator."""
        return self.page.locator(selector).inner_text()

    def wait_for_loader(self):
        """Common method to wait for the global app loader to disappear."""
        if self.global_spinner.is_visible():
            self.global_spinner.wait_for(state="hidden", timeout=15000)

    def verify_url(self, expected_url: str):
        """Common assertion used by Page Objects to verify they are on the right page."""
        expect(self.page).to_have_url(expected_url)

    def get_toast_message(self) -> str:
        """Returns text of success/error toast notifications."""
        self.toast_notification.wait_for(state="visible")
        return self.toast_notification.inner_text()