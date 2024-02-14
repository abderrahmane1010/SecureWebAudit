#!/usr/bin/python3

from secure_web_audit.csrf_analyzer import CSRFAnalyzer
from secure_web_audit.utils import *
from pathlib import Path
import argparse

def parse_args():   
    parser = argparse.ArgumentParser(description='SecureWebAudit Tool')
    parser.add_argument('-u','--url', type=str, help='website to analyze') # add ,required=True if you want
    return parser.parse_args()


def run():
    args = parse_args()
    
    if args.url :
        banner(args.url)
        CSRFAnalyzer(args.url,"GET")
        
if __name__ == "__main__":
    run()