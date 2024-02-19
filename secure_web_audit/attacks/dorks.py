from ..utils import *
import requests
import random
import time
from bs4 import BeautifulSoup
from ..helpers.headers_utils import *
from googlesearch import search
from fake_useragent import UserAgent

# ref: https://github.com/spekulatius/infosec-dorks
class GoogleDorks :

    def __init__(self, url, method):
        self.url = url
        self.ua = UserAgent()
        # self.subdomains_discovery()
        self.config_files()
        self.db_files()
        self.backup_files()
        self.gitfolder()
        self.exposed_files()
        self.sqlerrors()

    def run_dorks(self, payload):
        # ua = UserAgent()
        try:
            for results in search(payload, lang="en", user_agent=self.ua.random):
                    print(results)
                    # time.sleep(random.uniform(1, 15))
        except Exception as e:
            print(e)
                
    def subdomains_discovery(self):
        subdomains = "site:*."+self.url+" -www"
        dorks_banner(subdomains,"Subdomains discovery")
        self.run_dorks(subdomains)
                

    def config_files(self):
        """ 
        This dork searches for configuration files on the specified target site. 
        Configuration files often contain sensitive information such as database 
        credentials, API keys, and server configurations.
        """
        config_files = "site:"+self.url+" ext:xml | ext:conf | ext:cnf | ext:reg | ext:inf | ext:rdp | ext:cfg | ext:txt | ext:ora | ext:env | ext:ini"
        dorks_banner(config_files,"Configuration files discovery")
        self.run_dorks(config_files)
        
    def db_files(self):
        """
        This dork helps to find database files on the specified target site. 
        Database files may contain valuable data and their exposure can lead to unauthorized access or data breaches.
        """
        db_files = "site:"+self.url+" ext:sql | ext:db | ext:dbf | ext:mdb | ext:sql.gz | ext:sql.gz | ext:db.gz | ext:db.gz"
        dorks_banner(db_files,"Database files discovery")
        self.run_dorks(db_files)
        
    def backup_files(self):
        """
        This dork is useful for discovering backup files on the specified target site. 
        Backup files are often created to store previous versions of files or data, 
        but if they are exposed, they may contain sensitive or outdated information.
        """
        backup_files = "site:"+self.url+" ext:bkf | ext:bkp | ext:bak | ext:old | ext:backup"
        dorks_banner(backup_files,"Backup files discovery")
        self.run_dorks(backup_files)
        
    def gitfolder(self):
        """
        This dork searches for instances of the ".git" folder on the specified target site, excluding results from GitHub. 
        The .git folder contains version control information and can potentially expose sensitive source code and configuration details, 
        leading to unauthorized access or code leaks.
        """
        gitfolder = 'inurl:"/.git" '+self.url+' -site:github.com'
        dorks_banner(gitfolder,".git folder")
        self.run_dorks(gitfolder)
        
    def exposed_files(self):
        """
        This dork helps to find various document file types on the specified target site. 
        Exposed documents may contain sensitive information such as passwords, 
        intellectual property, or confidential data.
        """
        exposed_files = "site:"+self.url+" ext:doc | ext:docx | ext:odt | ext:pdf | ext:rtf | ext:sxw | ext:psw | ext:ppt | ext:pptx | ext:pps | ext:csv"
        dorks_banner(exposed_files,"Exposed documents discovery")
        self.run_dorks(exposed_files)
        
    def sqlerrors(self):
        """
        This dork searches for SQL errors on the specified target site. 
        The presence of these errors in web pages may indicate vulnerabilities 
        that can be exploited by attackers 
        to gain unauthorized access to databases or execute malicious SQL queries.
        """
        sql_errors = 'site:'+self.url+' AND (intext:"sql syntax near" | intext:"syntax error has occurred" | intext:"incorrect syntax near" | intext:"unexpected end of SQL command" | intext:"Warning: mysql_connect()" | intext:"Warning: mysql_query()" | intext:"Warning: pg_connect()")'
        dorks_banner(sql_errors,"SQL errors")
        self.run_dorks(sql_errors)