import requests
import re
import json
import time
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class SearchResult:
    def __init__(self, result):
        self.width = result["width"]
        self.height = result["height"]
        self.thumbnail = result["thumbnail"]
        self.url = result["url"]
        self.image = result["image"]
        self.title = result["title"]


class ApiSearchResults:
    def __init__(self):
        self.search_results = list()

    def add_results(self, results):
        for result in results:
            self.search_results.append(SearchResult(result))


def search(keywords, print_results=False, max_request_num=100) -> ApiSearchResults:
    url = 'https://duckduckgo.com/'
    results = ApiSearchResults()
    params = {
        'q': keywords
    }

    logger.debug("Hitting DuckDuckGo for Token")

    #   First make a request to above URL, and parse out the 'vqd'
    #   This is a special token, which should be used in the subsequent request
    res = requests.post(url, data=params)
    search_obj = re.search(r'vqd=([\d-]+)&', res.text, re.M | re.I)

    if not search_obj:
        logger.error("Token Parsing Failed !")
        return results

    logger.debug("Obtained Token")

    headers = {
        'dnt': '1',
        'accept-encoding': 'gzip, deflate, sdch, br',
        'x-requested-with': 'XMLHttpRequest',
        'accept-language': 'en-GB,en-US;q=0.8,en;q=0.6,ms;q=0.4',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 '
                      'Safari/537.36',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'referer': 'https://duckduckgo.com/',
        'authority': 'duckduckgo.com',
    }

    params = (
        ('l', 'wt-wt'),
        ('o', 'json'),
        ('q', keywords),
        ('vqd', search_obj.group(1)),
        ('f', ',,,'),
        ('p', '2')
    )

    request_url = url + "i.js"

    logger.debug("Hitting Url : %s", request_url)

    for i in range(0, max_request_num):
        data = _get_data(request_url, headers, params)
        logger.debug("Hitting Url Success : %s", request_url)
        if print_results:
            print_json(data["results"])
        results.add_results(data["results"])

        if "next" not in data:
            logger.debug("No Next Page - Exiting")
            break

        request_url = url + data["next"]
    return results


def _get_data(request_url, headers, params):
    while True:
        try:
            res = requests.get(request_url, headers=headers, params=params)
            data = json.loads(res.text)
            return data
        except ValueError:
            logger.debug("Hitting Url Failure - Sleep and Retry: %s", request_url)
            time.sleep(5)
            continue
    return None


def print_json(objs):
    for obj in objs:
        print("Width {0}, Height {1}".format(obj["width"], obj["height"]))
        print("Thumbnail {0}".format(obj["thumbnail"]))
        print("Url {0}".format(obj["url"]))
        print("Title {0}".format(obj["title"].encode('utf-8')))
        print("Image {0}".format(obj["image"]))
        print("__________")
