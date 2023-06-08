import csv
from typing import List, Tuple


class UniqueCompany:
    @staticmethod
    def get_unique_companies(csv_file_name: str) -> List[Tuple[str, str]]:
        unique_companies = set()

        with open(csv_file_name, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                unique_companies.add((row["company_name"], row["company_url"]))

        return list(unique_companies)

    @staticmethod
    def save_unique_companies_to_csv(
        unique_companies: List[Tuple[str, str]],
        output_csv_file_name: str = "filters/unique_companies.csv",
    ) -> None:
        with open(output_csv_file_name, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["company_name", "company_url"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for company_name, company_url in unique_companies:
                writer.writerow(
                    {"company_name": company_name, "company_url": company_url}
                )
