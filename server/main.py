from driver import Scraper, FileManager
from flask import Flask

HOST = "127.0.0.1"
PORT = 8000

'''
filemanager = FileManager('./data/auto/ips7777.txt')
filemanager.new()
filemanager.dump(scraper.filter_7777())
'''

api = Flask(__name__)
@api.route('/', methods=['GET'])
def peers():
    scraper = Scraper("https://cspr.live/tools/peers", 23, 10, 6)
    scraper.scrape(10000)
    return scraper.filter_7778()

@api.route('/test', methods=['GET'])
def test_peers():
    scraper = Scraper("https://testnet.cspr.live/tools/peers", 23, 10, 6)
    scraper.scrape(10000)
    return scraper.filter_7778()

def main():
    api.run(threaded=True, host=HOST, port=PORT)

main()