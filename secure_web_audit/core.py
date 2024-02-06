from .detector import detect_anomalies
from .analyzer import analyze_packets
from .header_analyzer import HeaderAnalyzer
from .csrf_analyzer import CSRFAnalyzer
from .webanalyzer import WebAnalyzer
from secure_web_audit.webpagecontent_analyzer import WebPageContent
from .xss_analyzer import XSSAnalyzer
from .utils import *
from pathlib import Path
import argparse

def parse_args():   
    parser = argparse.ArgumentParser(description='SecureWebAudit Tool')
    parser.add_argument('-u','--url', type=str, help='website to analyze') # add ,required=True if you want
    parser.add_argument('-g','--group_url', type=str, help='websites to analyze')
    return parser.parse_args()


def run():
    args = parse_args()
    
    if args.url :
        banner(args.url)
        """ Header Analysis """
        # HeaderAnalyzer(args.url)
        
        """ XSS Analysis """
        # XSSAnalyzer(args.url)
        
        """ Web page content - Information Gathering"""
        # WebPageContent(args.url)
        
        """ CSRF Analysis """
        # CSRFAnalyzer(args.url)
        
        """ tests """
        WebAnalyzer(args.url, "GET")

    if args.group_url :
        if Path(args.group_url).is_file():
            with open(args.group_url, 'r') as file:
                for line in file:
                    clean_line = line.strip()
                    print(clean_line)
                    # XSS Analyzer
                    XSSAnalyzer(clean_line)
        else:
            print("The file does not exist ")