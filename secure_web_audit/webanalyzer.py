from .utils import *
import requests
import json
from bs4 import BeautifulSoup, Comment
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
            
            # print(self.get_form_data())
            # print(colorize(json.dumps(self.get_form_data(), indent=4),"info"))
            
            self.brute_force_form_file(0, "resources/38650-username-sktorrent.txt")
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

                # print(f"[Form {form_id}] Method: {form_info['method']} - Action: {form_info['action']}")

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
        # print(colorize(f'Send request to form {form["id"]}',"green"))
        
        form_url = urljoin(self.url, form["action"])
        data = {field["name"]: data_name for field in form["fields"]}
        print(data)
        if form["method"] == "POST":
            response1 = requests.post(form_url, data=data)
        elif form["method"] == "GET":
            response1 = requests.get(form_url, params=data)
        
        return response1
        # html_content = BeautifulSoup(response1.text, 'html.parser')
        
        # print(colorize(f'{hash(str(response1.text))}',"magenta"))

    def brute_force_form_file(self, index, file):
        with open(file, 'r', encoding='latin-1') as file:
            for ligne in file:
                res = self.send_req_to_form(index, ligne.strip())
                print(colorize(f'{hash(str(res.text))}',"magenta"))