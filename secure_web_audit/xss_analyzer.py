from .utils import *
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urljoin

# example : http://sudo.co.il/xss/level0.php

class XSSAnalyzer :

    def __init__(self, url):
        self.url = url 
        self.find_user_inputs()
        banner_xss(url)
        
    def find_user_inputs(self):
        xss_test_script = "testforxssplease"
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        forms = soup.find_all('form')

        for form in forms:
            method = form.get('method', 'get').lower()  
            action = form.get('action') or self.url
            # print(f"Form found with method: {method}, action: {action}")
            form_url = urljoin(self.url, action)
            
            data = {input_tag.get('name'): xss_test_script for input_tag in form.find_all('input') if input_tag.get('name')}
            if method == "post":
                response1 = requests.post(form_url, data=data)
            elif method == "get":
                response1 = requests.get(form_url, params=data)
            
            if xss_test_script in response1.text:
                print(colorize(f"Possible XSS vulnerability detected at {form_url}","error"))

            # soup1 = BeautifulSoup(response1.text, 'html.parser')

            # print(f"Response to {method.upper()} request to {form_url}: {response1}")
            
        parsed_url = urlparse(self.url)
        params = parse_qs(parsed_url.query)
        if len(params) != 0 :
            data = {}
            for param in params:
                # print(f"URL parameter found: {param}")
                data[param] = xss_test_script
            response1 = requests.get(self.url, params=data)
            if xss_test_script in response1.text:
                print(colorize(f"Possible XSS vulnerability detected at {self.url}","error"))