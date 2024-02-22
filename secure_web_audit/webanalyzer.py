from .utils import *
import requests
import json
from bs4 import BeautifulSoup, Comment
from .helpers.headers_utils import *
from urllib.parse import urlparse, parse_qs, urljoin

# https://requests.readthedocs.io/en/latest/

# https://api.agify.io/?name=zabzab
# https://api.genderize.io/?name=marie
# https://api.nationalize.io/?name=jean

# https://rapidapi.com/search/security

class WebAnalyzer :

    def __init__(self, url, method):
        self.url = url
        try:
            res = requests.request(method=method, url=self.url, params={"name":"alo"})
            self.soup = BeautifulSoup(res.text, 'html.parser')
            
            """ Get all forms in the page """
            # print(self.get_form_data())
            # print(colorize(json.dumps(self.get_form_data(), indent=4),"info"))
     
            """ Send a request """
            # response = self.send_req_to_form(0,"admin")
            
            """ Example of brute force attack """
            # self.brute_force_form_file(0, "resources/38650-username-sktorrent.txt")
            
            """ Example of treating a response """
            # res = self.send_req_to_form(0,"test")
            # write_headers(res)
            # res1 = self.send_req_to_form(0,"test1")
            # write_headers(res1)
            
            
            """ Example of treating a response (with two datas)"""
            # res = self.send_two_data(0,"abtygtb","tbaaba")
            # write_headers(res)
            # res1 = self.send_two_data(0,"test","test")
            # write_headers(res1)
            # """ Headers difference """
            # headers_diff(res,res1)
            # """ HTML Content difference """
            # html_content_diff(res,res1)
            
            """ Search for information disclosure files"""
            self.check_info_files()
            
            # self.soup = BeautifulSoup(self.response.text, 'html.parser')
        except requests.exceptions.HTTPError as errh:
            print(colorize("Http Error:","error"),errh)
        except requests.exceptions.URLRequired as errh:
            print(colorize("Unvalid URL","error"))
        except requests.exceptions.ConnectionError as errc:
            print(colorize("Error Connecting:","error"),errc)
        except requests.exceptions.Timeout as errt:
            print(colorize("Timeout Error:","error"),errt)
        except requests.exceptions.RequestException as err:
            print(colorize("Error:","error"),err)


        """
        [
            {
                "id": "Form_1",
                "method": "POST",
                "action": "search.php?test=query",
                "fields": [
                    {
                        "name": "searchFor",
                        "type": "text"
                    }
                ]
            }
        ]

        """
    def get_form_data(self):
            forms = self.soup.find_all('form')
            
            form_struct = []

            for form in forms:
                form_id = form.get('name') or f'Form_{len(form_struct) + 1}'
                form_info = {
                    'id' : form_id,
                    'method': form.get('method', 'GET').upper(),
                    'action': form.get('action', ''),
                    'fields': []
                }

                for inp in form.find_all('input'):
                    if inp.get('type') and inp.get('type').lower() != 'submit':
                        field_info = {
                            'name': inp.get('name', ''),
                            'type': inp.get('type', '')
                        }
                        form_info['fields'].append(field_info)

                form_struct.append(form_info)

            return form_struct
        

            
    def send_req_to_form(self, index, data_name):
        form = self.get_form_data()[index]
        
        
        form_url = urljoin(self.url, form["action"])
        data = {field["name"]: data_name for field in form["fields"] if field["type"] != 'hidden'}
        print(data)
        if form["method"] == "POST":
            response1 = requests.post(form_url, data=data)
        elif form["method"] == "GET":
            response1 = requests.get(form_url, params=data)
        
        return response1
    
    def send_two_data(self, index, text1, text2):
        form = self.get_form_data()[index]
        form_url = urljoin(self.url, form["action"])
        data = {form['fields'][0]['name'] : text1, form['fields'][1]['name'] : text2}
        print(data)
        if form["method"] == "POST":
            response = requests.post(form_url, data=data)
        elif form["method"] == "GET":
            response = requests.get(form_url, params=data)
        return response

    def brute_force_form_file(self, index, file):
        with open(file, 'r', encoding='latin-1') as file:
            for ligne in file:
                res = self.send_req_to_form(index, ligne.strip())
                print(colorize(f'{hash(str(res.text))}',"magenta"))
                

    def check_info_files(self):
        file_paths = ["robots.txt", "sitemap.xml", "humans.txt", ".well-known/security.txt", "security.txt"]
        for file in file_paths:
            url = f"{self.url}/{file}"
            try:
                res = requests.get(url)
                if res.status_code == 200:
                    print(colorize(f"Un fichier {file} existe","red"))
                else:
                    print(f"le fichier {file} n'existe pas")
            except requests.RequestException as e:
                print(f"Erreur lors de la requête pour {url}: {e}")