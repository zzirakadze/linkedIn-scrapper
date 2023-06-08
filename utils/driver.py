import logging
from typing import List, Tuple
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class DriverUtils:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Initializing {__name__} class")

    def find_element(self, locator: Tuple[str, str], timeout: int = 10) -> WebElement:
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except Exception as e:
            self.logger.error(f"An error occurred while finding element {locator}: {e}")
            raise

    def find_elements(
        self, locator: Tuple[str, str], timeout: int = 10
    ) -> List[WebElement]:
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
            return elements
        except Exception as e:
            self.logger.error(
                f"An error occurred while finding elements {locator}: {e}"
            )
            raise

    def wait_until_clickable_and_click(
        self, locator: Tuple[str, str], timeout: int = 10
    ):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
        except Exception as e:
            self.logger.error(
                f"An error occurred while waiting for element {locator} to be clickable and clicking on it: {e}"
            )
            raise
