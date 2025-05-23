import requests
from bs4 import BeautifulSoup

class WebsiteManager:

    @staticmethod
    def scrape_website_morthdata(url):
        url = 'https://www.northdata.de/BBM+Einrichtungshaus+GmbH,+Parchim/Amtsgericht+Schwerin+HRB+12762'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')

        chart_elements = soup.find_all("div", class_="column bar-charts")

        #column bar-charts
        #drill-downs charts ui grey segment

        for elem in chart_elements:
            return elem.prettify

