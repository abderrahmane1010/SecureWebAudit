# Web Server Version Detection
import requests
from ..utils import *
from urllib.parse import urlparse, parse_qs, urljoin

class PathTraversal :
    
    def __init__(self, url):
        banner_analysis("Path traversal Analysis", url)
        self.url = url
        self.path_traversal_analysis()
        
    def path_traversal_analysis(self):
        with open('resources/lfi.txt', 'r', encoding='latin-1') as file:
            for ligne in file:
                url = self.url + ligne.strip()
                res = requests.get(url)
                if res.status_code == 200:
                    info_value(url, hash(res.text))
                else:
                    print(url)