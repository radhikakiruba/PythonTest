import pytest
from playwright.sync_api import Page, expect

from tests.pages.document_page import DocumentPage

class TestPage:
    @pytest.fixture(autouse=True)
    def setup(self, document_page):
        """This runs before every test in the class."""
        self.doc_page = document_page
        pass

    def test_doc_upload(self):
        self.doc_page.navigate()
        data="tests/data/AMemory.pdf"
        self.doc_page.upload_and_wait(data)
        expect(
            self.doc_page.success_text
        ).to_be_visible()


