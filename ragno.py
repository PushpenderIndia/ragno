
import subprocess
import requests
import argparse
import numpy as np
import threading

BLUE, RED, WHITE, YELLOW, MAGENTA, GREEN, END = '\33[94m', '\033[91m', '\33[97m', '\33[93m', '\033[1;35m', '\033[1;32m', '\033[0m'

"""
Crawl Source:
=============
1. web.archive.org
2. index.commoncrawl.org
3. otx.alienvault.com  [Under Dev]
"""
    
def get_arguments():
    parser = argparse.ArgumentParser(description=f'{RED} Ragno v1.0')
    parser._optionals.title = f"{GREEN}Optional Arguments{YELLOW}"
    parser.add_argument("-o", "--output", dest="output", help="Save Result in TXT file")
    parser.add_argument("-s", "--subs", dest="want_subdomain", help="Include Result of Subdomains", action='store_true')
    parser.add_argument("-q", "--quiet", dest="quiet", help="Run Scan Without printing URLs on screen", action='store_true')
    parser.add_argument("--deepcrawl", dest="deepcrawl", help=f"Uses All Available APIs of CommonCrawl for Crawling URLs [{WHITE}Takes Time{YELLOW}]", action='store_true')
    parser.add_argument("-t", "--thread", dest="thread", help=f"Number of Threads to Used. Default=50 [{WHITE}Use When deepcrawl is Enabled{YELLOW}]", default=50)    
    
    required_arguments = parser.add_argument_group(f'{RED}Required Arguments{GREEN}')
    required_arguments.add_argument("-d", "--domain", dest="domain", help="Target Domain Name, ex:- google.com")
    return parser.parse_args()
  

class PassiveCrawl:
    def __init__(self, domain, want_subdomain, threadNumber, deepcrawl):
        self.domain = domain
        self.want_subdomain = want_subdomain  #Bool
        self.deepcrawl = deepcrawl            #Bool
        self.threadNumber = threadNumber
        self.final_url_list = []
    
    def start(self):
        if self.deepcrawl:
            self.startDeepCommonCrawl()
        else:
            self.getCommonCrawlURLs(self.domain, self.want_subdomain, ["http://index.commoncrawl.org/CC-MAIN-2018-22-index"])
        
        urls_list1 = self.getWaybackURLs(self.domain, self.want_subdomain)
        urls_list2 = self.getOTX_URLs(self.domain)
        
        # Combining all URLs list
        self.final_url_list.extend(urls_list1)
        self.final_url_list.extend(urls_list2)
        
        # Removing Duplicate URLs
        self.final_url_list = list(dict.fromkeys(self.final_url_list))
        
        return self.final_url_list
    
    def getIdealDomain(self, domainName):
        final_domain = domainName.replace("http://", "")
        final_domain = final_domain.replace("https://", "")
        final_domain = final_domain.replace("/", "")
        final_domain = final_domain.replace("www", "")
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
        urls_list.pop(0)
        
        final_urls_list = []
        for url in urls_list:
            final_urls_list.append(url[0])    

        return final_urls_list
        
    def getOTX_URLs(self, domain):
        url = f"https://otx.alienvault.com/api/v1/indicators/hostname/{domain}/url_list"
        raw_urls = self.make_GET_Request(url, "json")
        urls_list = raw_urls["url_list"]
        
        final_urls_list = []
        for url in urls_list:
            final_urls_list.append(url["url"])
            
        return final_urls_list         

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
        
        final_urls_list = []
        
        for api in apiList:
            #url = f"http://index.commoncrawl.org/CC-MAIN-2018-22-index?url={wild_card+domain}/*&fl=url"  
            url = f"{api}?url={wild_card+domain}/*&fl=url"     
            raw_urls = self.make_GET_Request(url, "text")
                    
            if ("No Captures found for:" not in raw_urls) and ("<title>" not in raw_urls):
                urls_list = raw_urls.split("\n")

                for url in urls_list:
                    if url != "":
                        self.final_url_list.append(url)          
    
if __name__ == '__main__':
    arguments = get_arguments() 
    
    # Making Instance of PassiveCrawl Class
    crawl = PassiveCrawl(arguments.domain, arguments.want_subdomain, arguments.thread, arguments.deepcrawl)
    final_url_list = crawl.start()
    
    # If Quiet Mode is Enabled, Save URLs in TXT File, Else Print URLS
    if arguments.quiet:
        if arguments.output:
            with open(arguments.output, "w", encoding="utf-8") as f:
                for url in final_url_list:
                    f.write(url+"\n")
        else:
            with open(arguments.domain+".txt", "w", encoding="utf-8") as f:
                for url in final_url_list:
                    f.write(url+"\n") 
                    
    else:
        for url in final_url_list:
            print(url)
        print("[>> Total URLs] : ", len(final_list))  
        
    if arguments.output:
        with open(arguments.output, "w", encoding="utf-8") as f:
            for url in final_url_list:
                f.write(url+"\n")
                
        
       


