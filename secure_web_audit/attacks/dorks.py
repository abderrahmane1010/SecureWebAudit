from ..utils import *
import requests
from bs4 import BeautifulSoup
from ..helpers.headers_utils import *
from googlesearch import search
from fake_useragent import UserAgent

# https://www.google.com/search?q=site%3A*.lidl.com+-www.lidl.com
class GoogleDorks :

    def __init__(self, url, method):
        self.url = url
        self.ua = UserAgent()
        self.subdomains_discovery()


    def subdomains_discovery(self):
            subdomains = "site:*."+self.url+" -www"
            try:
                for results in search(subdomains, lang="en", user_agent=self.ua.random):
                    print(results)
            except Exception as e:
                print(e)