from .utils import *
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urljoin

# example : http://sudo.co.il/xss/level0.php

class XSSAnalyzer :

    def __init__(self, url):
        self.url = url 
        # banner_xss(url)
        self.find_possible_injection()
        
        
    def find_possible_injection(self):
        xss_test_script = "texthuihaobzaoibzhauihbzuiahbizha"
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
            
            html_content = BeautifulSoup(response1.text, 'html.parser')
            
            if xss_test_script in response1.text:
                print(colorize(f" [Form] Possible XSS vulnerability detected at {form_url}","error"))
                mot = html_content.find(string=xss_test_script)
                if mot :
                    parent = mot.find_parent()
                    if parent :
                        print(colorize(f'HTML CODE : {parent.find_parent()}',"magenta"))
                    else :
                        print(colorize(f'HTML CODE : {parent}',"magenta"))
                script_tag = html_content.find_all('script')
                for s in script_tag :
                    if xss_test_script in s.text :
                        print(colorize(f'SCRIPT : {s.prettify()}',"magenta"))
            
        parsed_url = urlparse(self.url)
        params = parse_qs(parsed_url.query)
        if len(params) != 0 :
            data = {}
            for param in params:
                data[param] = xss_test_script
            response2 = requests.get(self.url, params=data)
            html_content1 = BeautifulSoup(response2.text, 'html.parser')
            if xss_test_script in response2.text:
                print(colorize(f" [Params] Possible XSS vulnerability detected at {self.url}","error"))
                mot = html_content1.find(string=xss_test_script)
                if mot :
                    parent = mot.find_parent()
                    if parent :
                        print(colorize(f'HTML CODE : {parent.find_parent()}',"magenta"))
                    else :
                        print(colorize(f'HTML CODE : {parent}',"magenta"))
                        
                script_tag1 = html_content1.find_all('script')
                for s in script_tag1 :
                    if xss_test_script in s.text :
                        print(colorize(f'SCRIPT : {s.prettify()}',"magenta"))