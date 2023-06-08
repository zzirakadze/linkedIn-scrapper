import csv
import re

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from utils.driver import DriverUtils
from selenium.webdriver.remote.webdriver import WebDriver


class EmployeeAndVacancies:
    EMPLOYEE_COUNT_INFO = (
        By.CSS_SELECTOR,
        ".artdeco-carousel__title.ember-view>div>h2",
    )
    OPEN_VACANCIES_COUNT_INFO = (
        By.CSS_SELECTOR,
        ".org-jobs-job-search-form-module__headline",
    )

    def get_total(self, driver: WebDriver, csv_file: str) -> None:
        driver_utils = DriverUtils(driver)
        with open(csv_file, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            list_of_company_names = []
            list_of_urls = []
            for row in reader:
                list_of_company_names.append(row["company_name"])
                list_of_urls.append(row["company_url"])
        with open(
            "employees_and_vacancies_count.csv", "w", newline="", encoding="utf-8"
        ) as output_file:
            fieldnames = [
                "company_name",
                "total_amount_of_employees",
                "open_vacancies_count",
            ]
            writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            writer.writeheader()

            for name, url in zip(list_of_company_names, list_of_urls):
                people_page = url.replace("/life/", "/people/")
                jobs_page = url.replace("/life/", "/jobs/")
                driver.get(people_page)
                print(name)
                try:
                    total_amount_of_employees = driver_utils.find_element(
                        self.EMPLOYEE_COUNT_INFO, timeout=5
                    ).text
                    numbers = re.findall(r"\d+", total_amount_of_employees)
                    total_amount_of_employees = int("".join(numbers))
                except TimeoutException as ex:
                    total_amount_of_employees = "N/A"
                    print(f" The 'People' filter is not available for {name}", ex)

                driver.get(jobs_page)
                try:
                    open_vacancies_text = driver_utils.find_element(
                        self.OPEN_VACANCIES_COUNT_INFO, timeout=5
                    ).text
                    numbers = re.findall(r"\d+", open_vacancies_text)
                    open_vacancies_count = int("".join(numbers))
                except TimeoutException as ex:
                    open_vacancies_count = "N/A"
                    print(f" The 'Jobs' filter is not available for {name}", ex)

                writer.writerow(
                    {
                        "company_name": name,
                        "total_amount_of_employees": total_amount_of_employees,
                        "open_vacancies_count": open_vacancies_count,
                    }
                )
