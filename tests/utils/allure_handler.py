import logging
import allure

class AllureLoggerHandler(logging.Handler):
    def emit(self, record):
        if record.levelno >= logging.INFO:
            # This creates a step in Allure named after your log message
            with allure.step(f"LOG ({record.levelname}): {record.getMessage()}"):
                pass