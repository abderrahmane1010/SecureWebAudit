from ..utils import *
import difflib

def write_headers(response):
    headers = response.headers
    print(colorize(f'Number of headers : {len(headers)}',"cyan"))
    for header in headers:
        print(colorize(f'{header}',"green"), colorize(f'{headers[header]}',"info"))
        
# Caculate the leakage of informations => (break of confidentiality)
def headers_diff(response1, response2):
    """
    Diff of dicts :
    >>> dict1 = {1:'donkey', 2:'chicken', 3:'dog'}
    >>> dict2 = {1:'donkey', 2:'chimpansee', 4:'chicken'}
    >>> set1 = set(dict1.items())
    >>> set2 = set(dict2.items())
    >>> set1 ^ set2
        {(2, 'chimpansee'), (4, 'chicken'), (2, 'chicken'), (3, 'dog')}
    >>> set1 - set2
        {(2, 'chicken'), (3, 'dog')}
    >>> set2 - set1
        {(2, 'chimpansee'), (4, 'chicken')}
    """
    print(colorize(f'{set(response2.headers.items()) - set(response1.headers.items())}',"red"))
    
    
def html_content_diff(response1, response2):
    differ = difflib.Differ()
    # diff = differ.compare(response1.text.splitlines(keepends=True), response2.text.splitlines(keepends=True))
    """ + : present in the second (not the first) 
    / - : present in the first (not the second)"""
    exist_in_first = ''.join([line for line in differ.compare(response1.text.splitlines(keepends=True), response2.text.splitlines(keepends=True)) if line.startswith('-')])
    exist_in_second = ''.join([line for line in differ.compare(response1.text.splitlines(keepends=True), response2.text.splitlines(keepends=True)) if line.startswith('+')])  
    print(colorize(f'{exist_in_first}',"cyan"))
    print(colorize(f'{exist_in_second}',"green"))
