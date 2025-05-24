import requests
from bs4 import BeautifulSoup
import re

class WebsiteManager:

    @staticmethod
    def scrape_website_northdata(url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')

        chart_elements = soup.find_all("div", class_="column bar-charts")

        #column bar-charts
        #drill-downs charts ui grey segment

        for elem in chart_elements:
            return elem.prettify()

    @staticmethod
    def scrape_website_any(url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')

        articles = soup.find_all("article")     

        # Step 2: Collect tags inside articles (to exclude later)
        article_text_elements = set()
        for article in articles:
            for tag in article.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6"]):
                article_text_elements.add(tag)      

        # Step 3: Extract all relevant text elements (outside articles)
        tags_to_extract = ["p", "h1", "h2", "h3", "h4", "h5", "h6"]
        texts = []      

        for tag in soup.find_all(tags_to_extract):
            # Skip if this tag is inside an article
            if tag in article_text_elements:
                continue        

            # Filter out headers with <svg>
            if tag.name.startswith("h") and tag.find("svg"):
                continue        

            # Filter out paragraphs with <a href=...>
            if tag.name == "p" and tag.find("a", href=True):
                continue        

            text = tag.get_text(strip=True)
            if text and len(text.split()) > 5:
                texts.append(text)      

        # Step 4: Optionally extract meaningful text from <article> too
        for article in articles:
            for tag in article.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6"]):
                # Apply same filters inside article
                if tag.name.startswith("h") and tag.find("svg"):
                    continue
                if tag.name == "p" and tag.find("a", href=True):
                    continue
                text = tag.get_text(strip=True)
                if text and len(text.split()) > 5:
                    texts.append(text)      

        final_text = "\n".join(texts)

        return final_text
