from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv

class WantedJobScrapper:
    def __init__(self):
        self.p = sync_playwright().start()
        self.browser = self.p.chromium.launch(headless=False)
        self.keywords = []
        self.result = []

    def add_keyword(self, keyword):
        if isinstance(keyword, list) == True:
            self.keywords = keyword
        elif isinstance(keyword, str) == True:
            self.keywords.append(keyword) 
        print(f"Keywords : {self.keywords}")

    def reset(self):
        self.keywords.clear()
        self.p.stop()

    def start(self):
        for keyword in self.keywords:
            print(f"Scrapper {keyword}...")
            page = self.browser.new_page()
            page.goto(f"https://www.wanted.co.kr/search?query={keyword}&tab=position")

            for x in range(5):
                time.sleep(3)
                page.keyboard.down("End")

            content = page.content()
            soup = BeautifulSoup(content, "html.parser")

            jobs = soup.find_all("div", class_="JobCard_container__zQcZs")
            jobs_db = []

            for job in jobs:
                link = f"https://www.wanted.co.kr{job.find('a')['href']}"
                title = job.find("strong", class_="JobCard_title___kfvj").text
                company_name = job.find("span", class_="CompanyNameWithLocationPeriod_CompanyNameWithLocationPeriod__company__ByVLu wds-nkj4w6").text
                reward = job.find("span", class_="JobCard_reward__oCSIQ").get_text(strip=True) if job.find("span", class_="JobCard_reward__oCSIQ") else ""
                # location = job.find("span", class_="CompanyNameWithLocationPeriod_CompanyNameWithLocationPeriod__location__4_w0l wds-nkj4w6").text

                job = {
                    "title":title,
                    "company_name":company_name,
                    # "location": location,
                    "reward":reward,
                    "link":link
                }
                jobs_db.append(job)

            self.result = jobs_db
        self.reset()

        return self.result



def extract_wandted_jobs(keyword):
    scrapper = WantedJobScrapper()
    scrapper.add_keyword(keyword)
    return scrapper.start()
    