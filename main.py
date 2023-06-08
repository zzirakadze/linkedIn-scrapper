import time
import csv
from datetime import datetime
from typing import List, Dict, Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from filters.total_employees_vacancies import EmployeeAndVacancies
from filters.each_employee_info import Employee
from filters.unique_companies import UniqueCompany


def init_driver(headless: bool) -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    return driver


class LinkedInScraper:
    EMAIL = "youremail@example.com"
    PASSWORD = "yourp@#$sword"
    SEARCH_URL = "https://www.linkedin.com/jobs/search/?keywords={job_name}&location={address_name}&refresh=true"

    def __init__(self, headless: bool = False):
        self.driver = init_driver(headless)
        self.csv_file_name = ""

    def login(self) -> None:
        self.driver.maximize_window()
        self.driver.get("https://www.linkedin.com/")

        time.sleep(1)

        email_input = self.driver.find_element(By.ID, "session_key")
        email_input.send_keys(self.EMAIL)

        password_input = self.driver.find_element(By.ID, "session_password")
        password_input.send_keys(self.PASSWORD)

        submit_button = self.driver.find_element(
            By.CSS_SELECTOR, 'button[data-id="sign-in-form__submit-btn"]'
        )
        submit_button.click()

    def get_job_ids(self) -> List[str]:
        jobs = self.driver.find_elements(
            By.CSS_SELECTOR, "ul.scaffold-layout__list-container div.job-card-container"
        )
        job_ids = [item.get_attribute("data-job-id") for item in jobs]
        return job_ids

    def scrape_job_ids(
        self, job_name: str, address_name: str, num_pages: int = 26
    ) -> List[str]:
        search_url = self.SEARCH_URL.format(
            job_name=job_name, address_name=address_name
        )
        self.login()
        self.driver.get(search_url)
        all_job_ids = []
        for i in range(2, num_pages + 1):
            for listItem in self.driver.find_elements(
                By.CSS_SELECTOR, "ul.scaffold-layout__list-container>li"
            ):
                self.driver.execute_script("arguments[0].scrollIntoView();", listItem)
            time.sleep(2)
            all_job_ids.extend(self.get_job_ids())
            time.sleep(2)
            next_button = self.driver.find_element(
                By.CSS_SELECTOR, f"button[aria-label='Page {i}']"
            )
            next_button.click()
        print(all_job_ids)
        return all_job_ids

    def get_job_info(self, job_id: str) -> Dict[str, Optional[str]]:
        self.driver.get(f"https://www.linkedin.com/jobs/view/{job_id}/")
        time.sleep(2)

        company_name_selector = (
            By.CSS_SELECTOR,
            ".jobs-unified-top-card__company-name>a",
        )
        exact_location_selector = (By.CSS_SELECTOR, ".jobs-unified-top-card__bullet")
        employee_count_selector = (
            By.CSS_SELECTOR,
            ".jobs-unified-top-card__job-insight>span",
        )
        vacancy_full_title_selector = (
            By.CSS_SELECTOR,
            ".jobs-unified-top-card__job-title",
        )
        salary_range_selector = (By.CSS_SELECTOR, "a[href='#SALARY']")
        job_remote_or_not_selector = (
            By.CSS_SELECTOR,
            ".jobs-unified-top-card__workplace-type",
        )

        company_name = self.driver.find_element(*company_name_selector).text
        company_url = self.driver.find_element(*company_name_selector).get_attribute(
            "href"
        )

        exact_location = self.driver.find_elements(*exact_location_selector)[0].text
        employee_count = self.driver.find_elements(*employee_count_selector)[1].text
        vacancy_full_title = self.driver.find_element(*vacancy_full_title_selector).text

        try:
            salary_range = self.driver.find_element(*salary_range_selector).text
        except:
            print(f"No salary range for job_id: {job_id}")
            salary_range = None

        try:
            job_remote_or_not = self.driver.find_element(
                *job_remote_or_not_selector
            ).text
        except:
            print(f"No job remote or not for job_id: {job_id}")
            job_remote_or_not = None

        return {
            "company_name": company_name,
            "company_url": company_url,
            "exact_location": exact_location,
            "employee_count": employee_count,
            "vacancy_full_title": vacancy_full_title,
            "salary_range": salary_range,
            "job_remote_or_not": job_remote_or_not,
        }

    def grab_all_info(
        self, job_ids: List[str], job_name: str, address_name: str
    ) -> None:
        self.csv_file_name = f"{job_name}_{address_name.replace('%20', '_')}_{datetime.now().strftime('%Y-%m-%d')}.csv"
        with open(self.csv_file_name, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = [
                "company_name",
                "company_url",
                "exact_location",
                "employee_count",
                "vacancy_full_title",
                "salary_range",
                "job_remote_or_not",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for job_id in job_ids:
                try:
                    job_info = self.get_job_info(job_id)
                    writer.writerow(job_info)
                except Exception as exc:
                    print(f"An error occurred: {exc}")

    def crawler(self):
        unique_companies = UniqueCompany.get_unique_companies(self.csv_file_name)
        UniqueCompany.save_unique_companies_to_csv(unique_companies)
        EmployeeAndVacancies().get_total(self.driver, "filters/unique_companies.csv")
        Employee().get_data(self.driver, "filters/unique_companies.csv")


if __name__ == "__main__":
    job_name = "laravel"
    address_name = "United%20Kingdom"
    scraper = LinkedInScraper(headless=False)
    job_ids = scraper.scrape_job_ids(job_name, address_name)
    scraper.grab_all_info(job_ids, job_name, address_name)
    scraper.crawler()
