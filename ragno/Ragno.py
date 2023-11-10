
import pyfiglet
import requests
import argparse
import numpy as np
import threading

from colorama import init
from colorama import Fore, Back, Style
init()

"""
Crawl Source:
=============
1. web.archive.org
2. index.commoncrawl.org
3. otx.alienvault.com  
"""
    
class PassiveCrawl:
    def __init__(self, domain, domain_list, want_subdomain, threadNumber, deepcrawl, is_quiet_mode, output):
        self.domain         = domain
        self.domain_list    = domain_list
        self.want_subdomain = want_subdomain  #Bool
        self.deepcrawl      = deepcrawl       #Bool
        self.is_quiet_mode = is_quiet_mode    #Bool
        self.output        = output

        self.threadNumber = threadNumber
        self.final_url_list    = []
        self.wayback_urls_list = []
        self.otx_urls_list     = []
    
    def start(self):
        if self.domain:
            self.crawl_urls(self.domain)
            # If Quiet Mode is Enabled, Save URLs in TXT File, Else Print URLS
            if self.output:
                with open(self.output, "w", encoding="utf-8") as f:
                    for url in self.final_url_list:
                        f.write(url+"\n")
            
            if not self.is_quiet_mode:            
                for url in self.final_url_list:
                    print(url)
                print("[>> Total URLs] : ", len(self.final_url_list))  
            return self.final_url_list
        
        elif self.domain_list:
            with open(self.domain_list) as f:
                all_domains = f.readlines()
                for domain in all_domains:
                    ideal_domain = self.crawl_urls(domain.strip()) 
                    if self.is_quiet_mode:
                        with open(ideal_domain+".txt", "w", encoding="utf-8") as f:
                            for url in self.final_url_list:
                                f.write(url+"\n")   
                    else:
                        for url in self.final_url_list:
                            print(url)
                        print("[>> Total URLs] : ", len(self.final_url_list))  
                    self.final_url_list = []


    def crawl_urls(self, domain):
        domain = self.getIdealDomain(domain)

        if self.deepcrawl:
            thread1 = threading.Thread(target=self.startDeepCommonCrawl)
        else:
            thread1 = threading.Thread(target=self.getCommonCrawlURLs, args=(domain, self.want_subdomain, ["http://index.commoncrawl.org/CC-MAIN-2018-22-index"]))
            
        # MultiThreaded
        thread2 = threading.Thread(target=self.getWaybackURLs, args=(domain, self.want_subdomain,))
        thread3 = threading.Thread(target=self.getOTX_URLs, args=(domain,))

        # Start the threads
        thread1.start()
        thread2.start()
        thread3.start()

        # Wait for all threads to complete
        thread1.join()
        thread2.join()
        thread3.join()

        # Combining all URLs list
        self.final_url_list.extend(self.wayback_urls_list)
        self.final_url_list.extend(self.otx_urls_list)
        self.wayback_urls_list = []
        self.otx_urls_list     = []
            
        # Removing Duplicate URLs
        self.final_url_list = list(dict.fromkeys(self.final_url_list))
        return domain
    
    def getIdealDomain(self, domainName):
        final_domain = domainName.replace("http://", "")
        final_domain = final_domain.replace("https://", "")
        final_domain = final_domain.replace("/", "")
        final_domain = final_domain.replace("www.", "")
        print("[>>>] Domain:", final_domain)
        return final_domain

    def split_list(self, list_name, total_part_num):
        """
        Takes Python List and Split it into desired no. of sublist
        """
        final_list = []
        split = np.array_split(list_name, total_part_num)
        for array in split:
            final_list.append(list(array))		
        return final_list

    def make_GET_Request(self, url, response_type):
        response = requests.get(url)
        
        if response_type.lower() == "json":
            result = response.json()
        else:
            result = response.text
        
        return result

    def getWaybackURLs(self, domain, want_subdomain):
        if want_subdomain == True:
            wild_card = "*."
        else:
            wild_card = ""
               
        url = f"http://web.archive.org/cdx/search/cdx?url={wild_card+domain}/*&output=json&collapse=urlkey&fl=original"  
        urls_list = self.make_GET_Request(url, "json")
        try:
            urls_list.pop(0)
        except:
            pass
        
        final_urls_list = []
        for url in urls_list:
            final_urls_list.append(url[0])    

        self.wayback_urls_list = final_urls_list
        
    def getOTX_URLs(self, domain):
        url = f"https://otx.alienvault.com/api/v1/indicators/hostname/{domain}/url_list"
        raw_urls = self.make_GET_Request(url, "json")
        urls_list = raw_urls["url_list"]
        
        final_urls_list = []
        for url in urls_list:
            final_urls_list.append(url["url"])
            
        self.otx_urls_list = final_urls_list

    def startDeepCommonCrawl(self):
        api_list =  self.get_all_api_CommonCrawl()
        collection_of_api_list = self.split_list(api_list, int(self.threadNumber)) 

        thread_list = []
        for thread_num in range(int(self.threadNumber)):   
            t = threading.Thread(target=self.getCommonCrawlURLs, args=(self.domain, self.want_subdomain, collection_of_api_list[thread_num],)) 
            thread_list.append(t)
            
        for thread in thread_list:
            thread.start()
        for thread in thread_list:
            thread.join()

    def get_all_api_CommonCrawl(self):
        url = "http://index.commoncrawl.org/collinfo.json"
        raw_api = self.make_GET_Request(url, "json")
        final_api_list = []
        
        for items in raw_api:
            final_api_list.append(items["cdx-api"])
        
        return final_api_list

    def getCommonCrawlURLs(self, domain, want_subdomain, apiList):
        if want_subdomain == True:
            wild_card = "*."
        else:
            wild_card = ""
        
        for api in apiList:
            #url = f"http://index.commoncrawl.org/CC-MAIN-2018-22-index?url={wild_card+domain}/*&fl=url"  
            url = f"{api}?url={wild_card+domain}/*&fl=url"     
            raw_urls = self.make_GET_Request(url, "text")
                    
            if ("No Captures found for:" not in raw_urls) and ("<title>" not in raw_urls):
                urls_list = raw_urls.split("\n")

                for url in urls_list:
                    if url != "":
                        self.final_url_list.append(url)          

def get_arguments():
    banner = pyfiglet.figlet_format("            Ragno")
    print(banner+"\n")
    parser = argparse.ArgumentParser(description=f'{Fore.RED}Ragno v1.6 {Fore.YELLOW}[Author: {Fore.GREEN}Pushpender Singh{Fore.YELLOW}] [{Fore.GREEN}https://github.com/PushpenderIndia{Fore.YELLOW}]')
    parser._optionals.title = f"{Fore.GREEN}Optional Arguments{Fore.YELLOW}"
    parser.add_argument("-o", "--output", dest="output", help="Save Result in TXT file")
    parser.add_argument("-s", "--subs", dest="want_subdomain", help="Include Result of Subdomains", action='store_true')
    parser.add_argument("-q", "--quiet", dest="quiet", help="Run Scan Without printing URLs on screen", action='store_true')
    parser.add_argument("--deepcrawl", dest="deepcrawl", help=f"Uses All Available APIs of CommonCrawl for Crawling URLs [{Fore.WHITE}Takes Time{Fore.YELLOW}]", action='store_true')
    parser.add_argument("-t", "--thread", dest="thread", help=f"Number of Threads to Used. Default=50 [{Fore.WHITE}Use When deepcrawl is Enabled{Fore.YELLOW}]", default=50)    
    
    required_arguments = parser.add_mutually_exclusive_group(required=True)
    required_arguments.add_argument("-d", "--domain", dest="domain", help="Target Domain Name, ex:- google.com")
    required_arguments.add_argument("-dl", "--domain-list", dest="domain_list", help="File Containing Domain, One domain in One line.")
    return parser.parse_args()

def main():
    arguments = get_arguments() 
    
    # Making Instance of PassiveCrawl Class
    crawl = PassiveCrawl(arguments.domain, 
                         arguments.domain_list, 
                         arguments.want_subdomain, 
                         arguments.thread, 
                         arguments.deepcrawl,
                         arguments.quiet,
                         arguments.output
                         )
    final_url_list = crawl.start()
    
if __name__ == '__main__':
    main()
                
        
       


