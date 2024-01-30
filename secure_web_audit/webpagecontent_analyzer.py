from .utils import *
import requests
from bs4 import BeautifulSoup, Comment


class WebPageContent :

    def __init__(self, url):
        self.url = url
        
        try:
            self.response = requests.get(self.url)
            self.soup = BeautifulSoup(self.response.text, 'html.parser')
            print(colorize(str(len(self.get_all_comments())) + " comments", "info"))
            print(self.get_all_comments())
            
        except requests.exceptions.HTTPError as errh:
            print(colorize("Http Error:","error"),errh)
        except requests.exceptions.ConnectionError as errc:
            print(colorize("Error Connecting:","error"),errc)
        except requests.exceptions.Timeout as errt:
            print(colorize("Timeout Error:","error"),errt)
        except requests.exceptions.RequestException as err:
            print(colorize("Error:","error"),err)


    def get_all_comments(self):
        return self.soup.find_all(string=lambda text: isinstance(text, Comment))