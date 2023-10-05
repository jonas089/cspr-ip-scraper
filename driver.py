from playwright.sync_api import sync_playwright
from lxml import html

IP_SELECTOR="xpath=/html/body/div[1]/div[2]/div[2]/div/div[2]/table/tbody/tr[{}]/td[2]"
BUTTON_SELECTOR="xpath=/html/body/div[1]/div[2]/div[2]/div/div[3]/div/div[2]/button[3]"

class Scraper:
    def __init__(self, url, pages, perpage, lastpage):
        self.url = url
        self.pages = pages
        self.perpage = perpage
        self.lastpage = lastpage
        self.ips = []
    def scrape(self, timeout_value):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(self.url)
            for i in range(0, self.pages-1):
                for j in range(1, self.perpage+1):
                    element = page.wait_for_selector(IP_SELECTOR.format(j))
                    ip = element.inner_text()
                    self.ips.append(ip)
                button = page.wait_for_selector(BUTTON_SELECTOR, timeout=timeout_value)
                button.click()
            for i in range(1, self.lastpage + 1):
                element = page.wait_for_selector(IP_SELECTOR.format(i), timeout=timeout_value)
                ip = element.inner_text()
                self.ips.append(ip)

    def filter_7777(self):
        if len(self.ips) == 0:
            return 0
        filtered = []
        for i, ip in enumerate(self.ips):
            x = ''
            for l in ip:
                if l != ':':
                    x += l
                else:
                    x += ':7777'
                    break
            filtered.append(x)
        return filtered
    def filter_raw(self):
        if len(self.ips) == 0:
            return 0
        filtered = []
        for i, ip in enumerate(self.ips):
            x = ''
            for l in ip:
                if l != ':':
                    x += l
                else:
                    break
            filtered.append(x)
        return filtered