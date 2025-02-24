#!/usr/bin/env python3
import httpx 
import os  
from colorama import Fore,Back,Style
import concurrent.futures 
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup
import time as t
import warnings
import random
from alive_progress import alive_bar
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import urllib3
import asyncio



warnings.simplefilter('ignore', requests.packages.urllib3.exceptions.InsecureRequestWarning)

warnings.filterwarnings("ignore")

red =  Fore.RED

green = Fore.GREEN

magenta = Fore.MAGENTA

cyan = Fore.CYAN

mixed = Fore.RED + Fore.BLUE

blue = Fore.BLUE

yellow = Fore.YELLOW

white = Fore.WHITE

reset = Style.RESET_ALL

bold = Style.BRIGHT

colors = [ green, cyan, blue]

random_color = random.choice(colors)



def save(url, args):
    
    try:
        
        if args.output:
        
        
            
            if os.path.isfile(args.output):
                
                filename = args.output
                
            elif os.path.isdir(args.output):
                
                filename = os.path.join(args.output, f"Dir_results.txt")
                
            else:
                
                filename = args.output
            
        
            with open(filename, "a") as w:
            
                w.write(url + '\n')

    except KeyboardInterrupt as e:
        
        print(f"\n[{bold}{blue}INFO{reset}]: {bold}{white}Probuster exits..{reset}")
        
        exit()
        
    except Exception as e:
        
        pass




def dirbust_req(url, args):
    
    try:
        
        warnings.filterwarnings("ignore", category=ResourceWarning)
        
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        requests.packages.urllib3.disable_warnings()

        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        
        proxies = {
            
            "http": f"{args.proxy}",
            "https": f"{args.proxy}"
        } if args.proxy else False
        
        
        timeout= args.timeout if args.timeout else 10
   
        response = requests.get(url, verify=False, timeout=timeout, proxies=proxies)   
        
        
        server1 =  response.headers.get("server")
        
        content_type = response.headers.get("Content-Type")
        
        if content_type:
            
            content_type = content_type.split(";")[0].strip()
            
            
        with warnings.catch_warnings():
                
                
                warnings.filterwarnings("ignore", category=UserWarning, module="bs4")
            
                soup = BeautifulSoup(response.content, "html.parser")
    
                text = soup.get_text() 
    
    
        word_count = len(text.split())  
            
        title = soup.title.string
        
        server = server1 if args.server else ""
                
        content = content_type if args.application_type else ""
                
        word =  word_count if args.word_count else ""
        
        title = title if args.title else ""
        
        
        
        if args.exclude and str(response.status_code) in args.exclude:
                
                pass
            
        if not args.exclude  and not args.match:
            
            
            if args.no_color:
            
                result = f"{url} [{response.status_code}] [{server}] [{content}] [{title}] [{word}]" 
                    
                print(f"{result}\n")
                
                save(result, args)
            
            else:
            
                result = f"{bold}{white}{url} [{bold}{blue}{response.status_code}{reset}] [{bold}{magenta}{server}{reset}] [{bold}{yellow}{content}{reset}] [{bold}{cyan}{title}{reset}] [{cyan}{word}{reset}]"
                    
                print(f"{result}\n")
                
                save(result, args)
        
        if args.exclude  and not args.match:
            
            if str(response.status_code) not in args.exclude:
            
                if args.no_color:
            
                    result = f"{url} [{response.status_code}] [{server}] [{content}] [{title}] [{word}]" 
                    
                    print(f"{result}\n")
            
                    save(result, args)
                    
                else:
            
                    result = f"{bold}{white}{url} [{bold}{blue}{response.status_code}{reset}] [{bold}{magenta}{server}{reset}] [{bold}{yellow}{content}{reset}] [{bold}{cyan}{title}{reset}] [{cyan}{word}{reset}]"
                    
                    print(f"{result}\n")
                    
                    save(result, args)
                    
        
        if args.match and str(response.status_code) in args.match:
                
                    if args.no_color:
            
                        result = f"{url} [{response.status_code}] [{server}] [{content}] [{title}] [{word}] " 
                        
                        print(f"{result}\n")
                        
                        save(result, args)
            
                    else:
            
                        result = f"{bold}{white}{url} [{bold}{blue}{response.status_code}{reset}] [{bold}{magenta}{server}{reset}] [{bold}{yellow}{content}{reset}] [{bold}{cyan}{title}{reset}] [{cyan}{word}{reset}]"
                        
                        print(f"{result}\n")
                        
                        save(result, args)
        
    except KeyboardInterrupt as e:
        
        print(f"\n[{bold}{blue}INFO{reset}]: {bold}{white}Probuster exits..{reset}")
        
        exit()
        
    except requests.RequestException as e:
        
        if args.verbose:
            
            print(f"[{bold}{red}TIME-OUT{reset}]: {bold}{white}{url}{reset}")
        
        
    except Exception as e:
        
        pass
            
            
def dirbust_threader(hosts,args) :
    
    try:
        
        global bar
        
        if args.show_progress:
        
            with alive_bar(len(hosts), enrich_print=False) as bar:
                
                try:
                    
                    
                    with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as executor:
                        
                       
                        futures = [executor.submit(dirbust_req,host, args) for host in hosts]

                        for futures in concurrent.futures.as_completed(futures):
                                
                            bar()
               
                
                except KeyboardInterrupt as e:
        
                    print(f"\n[{bold}{blue}INFO{reset}]: {bold}{white}Probuster exits..{reset}")
        
                    exit()
        
                except Exception as e:
        
            
                    pass
                            
        else:
            
            try:
                
                with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency)  as executor:
                    
            
                    futures = [executor.submit(dirbust_req,host, args) for host in hosts]
                    
                
                concurrent.futures.wait(futures)
                
                
            except KeyboardInterrupt as e:
        
                    print(f"\n[{bold}{blue}INFO{reset}]: {bold}{white}Probuster exits..{reset}")
        
                    exit()
        
            except Exception as e:
        
                    pass
                
                
    except KeyboardInterrupt as e:
        
        
        print(f"\n[{bold}{blue}INFO{reset}]: {bold}{white}Probuster exits..{reset}")
        
        
        exit()
        
    except Exception as e:
        
        pass
            



warnings.resetwarnings()