from ..utils import *

def write_headers(response):
    headers = response.headers
    print(colorize(f'Number of headers : {len(headers)}',"cyan"))
    for header in headers:
        print(colorize(f'{header}',"green"), colorize(f'{headers[header]}',"info"))
        
        
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