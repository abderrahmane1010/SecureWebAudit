from .utils import *
import requests
from bs4 import BeautifulSoup, Comment


class WebPageContent :

    def __init__(self, url):
        self.url = url
        
        try:
            self.response = requests.get(self.url)
            self.soup = BeautifulSoup(self.response.text, 'html.parser')
            
            # Comments
            # print(colorize(str(len(self.get_all_comments())) + " comments", "info"))
            # print(self.get_all_comments())
            
            # Meta
            self.get_all_meta()
            
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
    

    def get_all_meta(self):
        for tag in self.soup.find_all("meta"):
            property_value = tag.get("property", None)
            name_value = tag.get("name", None)
            content_value = tag.get("content", None)
            if property_value == "og:title":
                info_value("Title : ",content_value)
            elif property_value == "og:url":
                info_value("URL : ",content_value)
            elif property_value == "og:description":
                info_value("Description : ",content_value)
            elif property_value == "og:image":
                info_value("Image URL : ",content_value)
            elif property_value == "og:type":
                info_value("Type : ",content_value)
            elif name_value == "keywords":
                info_value("Keywords : ",content_value)
            elif name_value == "author":
                info_value("Author : ",content_value)
            elif name_value == "viewport":
                info_value("Viewport : ",content_value)
            elif tag.get("charset", None):
                info_value("Charset : ",tag.get('charset'))
            elif tag.get("http-equiv", None):
                info_value("HTTP-Equiv : ",tag.get('http-equiv'))
            elif property_value == "og:locale":
                info_value("Language : ",content_value)
            else:
                info_value("Autre Meta Tag : ",tag.attrs)
                
