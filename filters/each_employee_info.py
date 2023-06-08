import csv
import re
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from utils.driver import DriverUtils
from selenium.webdriver.remote.webdriver import WebDriver


class Employee:
    ALL_EMPLOYEES_LINK = (
        By.CSS_SELECTOR,
        ".ember-view.org-top-card-summary-info-list__info-item",
    )
    EMPLOYEES_LIST = (By.CSS_SELECTOR, ".search-results-container>div>div>ul>li")
    NAME_SELECTOR = (By.CSS_SELECTOR, ".entity-result__title-text")
    TITLE_SELECTOR = (By.CSS_SELECTOR, ".entity-result__primary-subtitle")
    LOCATION_SELECTOR = (By.CSS_SELECTOR, ".entity-result__secondary-subtitle")
    NEXT_BTN = (By.CSS_SELECTOR, "button[aria-label='Next']")

    def is_next_btn_enabled(self, driver_utils, next_btn_selector):
        try:
            next_btn = driver_utils.find_element(next_btn_selector)
            return next_btn.is_enabled()
        except Exception as e:
            print("Next button not found, INFO:", e)
            return False

    def get_data(self, driver: WebDriver, csv_file: str = "unique_companies.csv"):
        driver_utils = DriverUtils(driver)
        with open(csv_file, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            list_of_company_names = []
            list_of_urls = []
            for row in reader:
                list_of_company_names.append(row["company_name"])
                list_of_urls.append(row["company_url"])

        with open(
            "each_employee_report.csv", "w", newline="", encoding="utf-8"
        ) as output_file:
            fieldnames = [
                "company_name",
                "employee_name",
                "employee_position",
                "employee_location",
            ]
            writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            writer.writeheader()

            for name, url in zip(list_of_company_names, list_of_urls):
                people_page = url.replace("/life/", "/people/")
                driver.get(people_page)
                try:
                    driver_utils.wait_until_clickable_and_click(self.ALL_EMPLOYEES_LINK)
                except Exception as e:
                    print(
                        f"{name} does not provides such information related to people"
                    )
                    break
                employees = driver_utils.find_elements(self.EMPLOYEES_LIST)

                while True:
                    for index, employee in enumerate(employees):
                        try:
                            driver.execute_script(
                                "arguments[0].scrollIntoView();", employee
                            )
                        except Exception as e:
                            print(
                                "Exception occurred while scrolling into view, INFO: ",
                                e,
                            )
                        try:
                            employee_name = driver_utils.find_elements(
                                self.NAME_SELECTOR
                            )[index].text
                        except Exception as e:
                            print(
                                "Exception occurred while getting employee_name, INFO:",
                                e,
                            )
                        try:
                            employee_position = driver_utils.find_elements(
                                self.TITLE_SELECTOR
                            )[index].text
                        except Exception as e:
                            print(
                                "Exception occurred while getting employee_position, INFO:",
                                e,
                            )
                        try:
                            employee_location = driver_utils.find_elements(
                                self.LOCATION_SELECTOR
                            )[index].text
                        except Exception as e:
                            print(
                                "Exception occurred while getting employee_location, INFO:",
                                e,
                            )

                        writer.writerow(
                            {
                                "company_name": name,
                                "employee_name": employee_name.split("View")[0].strip(),
                                "employee_position": employee_position,
                                "employee_location": employee_location,
                            }
                        )

                    if self.is_next_btn_enabled(driver_utils, self.NEXT_BTN):
                        try:
                            next_btn = driver_utils.find_element(self.NEXT_BTN)
                            next_btn.click()
                            employees = driver_utils.find_elements(self.EMPLOYEES_LIST)
                        except Exception as e:
                            print(
                                "Exception occurred while clicking Next button, INFO:",
                                e,
                            )
                            break
                    else:
                        break
