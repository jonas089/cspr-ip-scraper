from driver import Scraper
scraper = Scraper("https://cspr.live/tools/peers", 23, 10, 6)
scraper.scrape(10000)
print(scraper.ips)
print(scraper.filter_raw())
print(scraper.filter_7777())