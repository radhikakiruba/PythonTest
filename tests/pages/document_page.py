from tests.pages.base_page import BasePage


class DocumentPage(BasePage):
    def __init__(self, page,config):
        # Call the parent constructor
        super().__init__(page,config)

        # Specific locators for this page
        self.choose_file=page.get_by_role("button", name="Choose File")
        self.upload_file=page.get_by_role("button", name="Upload")
        self.file_input = page.locator('input[type="file"]')
        self.chat_textarea = page.get_by_placeholder("Ask a question...")
        self.success_text = page.get_by_text("PDF uploaded and processed successfully")

    def upload_and_wait(self, file_path: str):
        self.logger.info(f"Upload file: {file_path}")
        self.choose_file.set_input_files(file_path)
        # Using a method inherited from BasePage
        self.wait_for_loader()
        self.upload_file.click()