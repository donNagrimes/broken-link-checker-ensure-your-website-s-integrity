thonimport requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import time
import logging

class BrokenLinkChecker:
    def __init__(self, base_url, max_pages=100, request_delay=1, max_concurrency=10):
        self.base_url = base_url
        self.max_pages = max_pages
        self.request_delay = request_delay
        self.max_concurrency = max_concurrency
        self.checked_links = set()
        self.broken_links = []

    def crawl(self, url, depth=0):
        if depth >= self.max_pages:
            return
        try:
            logging.info(f"Crawling URL: {url}")
            response = requests.get(url)
            if response.status_code != 200:
                self.broken_links.append({
                    'url': url,
                    'httpStatus': response.status_code,
                    'title': "N/A",
                    'referrer': "N/A"
                })
            else:
                soup = BeautifulSoup(response.text, 'html.parser')
                links = self.extract_links(soup, url)
                for link in links:
                    if link not in self.checked_links:
                        self.checked_links.add(link)
                        self.crawl(link, depth + 1)
            time.sleep(self.request_delay)
        except requests.RequestException as e:
            logging.error(f"Error crawling {url}: {e}")

    def extract_links(self, soup, base_url):
        links = set()
        for tag in soup.find_all('a', href=True):
            link = tag.get('href')
            full_url = urljoin(base_url, link)
            if full_url.startswith(self.base_url):
                links.add(full_url)
        return links

    def get_broken_links(self):
        return self.broken_links