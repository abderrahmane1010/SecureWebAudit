from .utils import *
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urljoin

class CSRFAnalyzer :

    token = None
    
    TOKEN_FORM_STRINGS = [
        "authenticity_token", # Commonly used by Ruby on Rails applications
        "_token", # Seen in various frameworks as a general-purpose token name
        "csrf_token", # Generic CSRF token name
        "csrfname", # Custom or less common CSRF token name
        "csrftoken", # Used by Django and some other Python frameworks
        "anticsrf", # Generic anti-CSRF token name, less commonly used
        "__requestverificationtoken", # Used by ASP.NET applications for CSRF protection
        "token", # Very generic token name that could be used for CSRF protection
        "csrf", # Short form for CSRF token names
        "_csrf_token", # Variation seen in some frameworks
        "xsrf_token", # Used by AngularJS and others for cross-site request forgery protection
        "_csrf", # Another common short form for CSRF token names
        "csrf-token", # Hyphenated form, used by some applications
        "xsrf-token", # Hyphenated form, specifically for XSRF tokens
        "_wpnonce", # Used by WordPress as a nonce token for protecting against CSRF and other types of attacks
        "csrfmiddlewaretoken", # Used by Django as part of its CSRF protection mechanism
        "__csrf_token__", # Double underscored, less common form for CSRF tokens
        "csrfkey" # Suggests a unique key for CSRF protection, less commonly used
    ]

    TOKEN_HEADER_STRINGS = [
        "csrf-token", "x-csrf-token", "xsrf-token", "x-xsrf-token", "csrfp-token",
        "anti-csrf-token", "x-csrf-header", "x-xsrf-header", "x-csrf-protection"
    ]
    def __init__(self, url):
        self.url = url 
        self.token_search_in_forms()
    
    
    def token_search_in_forms(self):
        """ Look if the token exists in all forms ?"""
        try:
            response = requests.get(self.url)
            soup = BeautifulSoup(response.text, 'html.parser')
            forms = soup.find_all('form')
            if len(forms) == 0:
                print(colorize("Aucun form trouvé","info"))
            counter = 1    
            for form in forms:
                form_id = form.get('name') if form.get('name') is not None else counter 
                print(colorize(f'[Form] #{form_id}',"info"))
                counter+=1
                form_token_counter=0
                all_inputs = form.find_all('input')
                for inp in all_inputs:
                    if inp.get('name') is not None and inp.get('name').lower() in self.TOKEN_FORM_STRINGS:
                        print(colorize(f"[Token found]","info"))
                        form_token_counter+=1
                        pass
                    elif inp.get('type') == 'hidden':
                        print(colorize(f"[Hiden type found]","info"))
                        form_token_counter+=1
                        pass
                if form_token_counter == 0:
                    print(colorize("[CSRF Info] Aucun CSRF token trouvée","error"))
                
        except requests.exceptions.HTTPError as errh:
            print(colorize("Http Error:","error"),errh)
        except requests.exceptions.ConnectionError as errc:
            print(colorize("Error Connecting:","error"),errc)
        except requests.exceptions.Timeout as errt:
            print(colorize("Timeout Error:","error"),errt)
        except requests.exceptions.RequestException as err:
            print(colorize("Error:","error"),err)
