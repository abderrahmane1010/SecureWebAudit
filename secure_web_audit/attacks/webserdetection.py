# Web Server Version Detection
import requests
from ..utils import *

class WebServerDetection :
    
    def __init__(self, url):
        banner_analysis("Web Server Detection", url)
        self.url = url
        self.headers = requests.get(self.url).headers
        self.server_detection()
        
    def server_detection(self):
        if "Server" in self.headers :
            print(self.headers["Server"])
        else :
            apache = ['Date', 'Server', 'Last-Modified', 'ETag', 'Accept-Ranges', 'Content-Length', 'Connection', 'Content-Type']
            nginx_or_other = ['Server', 'Date', 'Content-Type']
            headers = list(self.headers.keys())
            headers_order = [header for header in headers if header in apache or header in nginx_or_other]
            if headers_order == apache:
                print("apache")
            elif headers_order == nginx_or_other:
                print("nginx or other")
            else:
                print("other")