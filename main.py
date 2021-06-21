from colorama import Fore, Style, init; init()
from fake_useragent import UserAgent
from requests import Session, post
from threading import Thread
import time, random, sys

class CTB():
    def __init__(self, webhook):
        self.banned_proxy = []
        self.error_proxy  = []
        self.used_proxy   = []
        self.proxy_list   = []
        self.hook   = webhook
        self.banned = 0
        self.botted = 0
        self.error  = 0
        self.url = []
    
    '''
    Charger les fichiers dans les listes, et retirer les proxy/url dupliqués
        New:
            * Handle proxy / url not found
    '''
    def load_files(self):
        with open('./sources/url.txt', 'r') as url_file:
            for url in url_file:
                self.url.append(url.split('\n')[0])
        
        with open('./sources/proxy.txt', 'r') as proxy_file:
            for proxy in proxy_file:
                self.proxy_list.append(proxy.split('\n')[0])

        self.proxy_list = list(set(self.proxy_list))
        self.url        = list(set(self.url))

        if len(self.proxy_list) <= 5:
            print(f'[{Fore.LIGHTRED_EX}{time.strftime("%H:%M:%S", time.localtime())}{Fore.RED}] ERROR: not enought proxy found, 5 proxies required', end='\n')
            sys.exit(0)

        if len(self.url) == 0:
            print(f'[{Fore.LIGHTRED_EX}{time.strftime("%H:%M:%S", time.localtime())}{Fore.RED}] ERROR: not enought url found, 1 proxies required', end='\n')
            sys.exit(0)

    '''
    Envoyer une noctification sur discord avec les statistiques du bot
        New:
            * Banned proxy
            * New embed color
    '''
    def send_hook(self):
        try:
            post(self.hook, headers= {'content-type': 'application/json'}, json= {
                'content': None,
                'embeds': [
                            {
                                'color': 0x4077f8,
                                'fields': [
                                    {
                                    'name': '> ⭐ **Estimated earn:**',
                                    'value': f'```{self.botted * 0.0025}€```'
                                    },
                                    {
                                    'name': '> 🔵 **View sent:**',
                                    'value': f'```{self.botted}```'
                                    },
                                    {
                                    'name': '> 🔴 **Error:**',
                                    'value': f'```{self.error}```'
                                    },
                                    {
                                    'name': '> 🔴 **Banned:**',
                                    'value': f'```{self.banned}```'
                                    }
                                ],
                                'footer': {
                                    'text': 'CTB By Ѵιcнч\"RCΛ#1337 - github.com/Its-Vichy - discord.gg/rca',
                                    'icon_url': 'https://photos.angel.co/startups/i/7641023-67bf91ba0e7f458607f981d1813d0ef8-medium_jpg.jpg?buster=1614716185'
                                }
                            }
                        ],
                'username': 'CTB - Report',
                'avatar_url': 'https://photos.angel.co/startups/i/7641023-67bf91ba0e7f458607f981d1813d0ef8-medium_jpg.jpg?buster=1614716185'
            })
        except:
            pass

    '''
    Mettre à jour la console toute les secondes
        New:
            * Banned proxy
            * Error when price is so long
    '''
    def update_gui(self):
        while not len(self.used_proxy) == len(self.proxy_list):
            time.sleep(1)
            self.used_proxy  = list(set(self.used_proxy))
            self.error_proxy = list(set(self.error_proxy))
            print(f'[{Fore.LIGHTRED_EX}{time.strftime("%H:%M:%S", time.localtime())}{Fore.WHITE}] BOT: {Fore.GREEN}{self.botted}{Fore.WHITE} ERROR: {Fore.YELLOW}{self.error}{Fore.WHITE} BANNED: {Fore.LIGHTYELLOW_EX}{self.banned}{Fore.WHITE} USED PROXY: {Fore.LIGHTMAGENTA_EX}{len(self.used_proxy)}{Fore.WHITE}/{Fore.MAGENTA}{len(self.proxy_list)}{Fore.WHITE} EARN ~{Fore.CYAN}{self.botted * 0.0025}{Fore.WHITE}€             ', end='\r')
         
        BOT.send_hook()

    '''
    Un worker
        New:
            * Handle cloudfare ban
            * Spoof referer
    '''
    def worker(self, url, proxy_list):
        for proxy in proxy_list:
            if proxy not in self.error_proxy or proxy not in self.banned_proxy:
                self.used_proxy.append(proxy)

                try:
                    session = Session()
                    session.headers = {'user-agent': UserAgent().random, 'referer': 'https://' + random.choice(['github.com', 'discord.com', 'twitter.com', 'facebook.com', 'youtube.com'])}
                    session.proxies = {'http': proxy, 'https': proxy}
                    response = session.get('https://www.mylink1.biz/link/redirect/?url=' + session.get(url).text.split('https://www.mylink1.biz/link/redirect/?url=')[1].split('">')[0])

                    if response.status_code == 200:
                        if 'Cloudflare Ray' not in response.text:
                            self.botted += 1
                        else:
                            self.banned_proxy.append(proxy)
                            self.banned += 1
                    
                except:
                    self.error_proxy.append(proxy)
                    self.error += 1
    
    '''
    Obtennir les proportions parfaite entre chaque thread et chaque proxy
    '''
    def get_perfect_number(self, N):
        diviseurs = []

        for i in range(1, int(N / 2 + 1)):
            if not N%i:
                diviseurs.append(i)

        best = 1
        for i in diviseurs:
            if abs(i - N / i) < abs(best - N / best):
                best = i

        return best, int(N / best)

    '''
    Démarer tous les threads
        New:
            * Handle thread creation limit
    '''
    def start_worker(self):
        thread_list = []

        thread_list.append(Thread(target= self.update_gui))
        for url in self.url:
            for proxys in list(zip(*[iter(self.proxy_list)] * self.get_perfect_number(len(self.proxy_list))[1])):
                try:
                    thread_list.append(Thread(target= self.worker, args=(url, list(proxys),)))
                except:
                    break

        for thread in thread_list:
            thread.start()

        for thread in thread_list:
            thread.join()

if __name__ == '__main__':
    print(Style.BRIGHT + Fore.LIGHTRED_EX + f'''  
   ___ _____ ___ 
  / __|_   _| _ )
 | (__  | | | _ \\
  \___| |_| |___/  Ѵιcнч"RCΛ#1337 | https://github.com/Its-Vichy | discord.gg/rca
                 

    ''' + Style.RESET_ALL)

    while True:
        BOT = CTB('https://discord.com/api/webhooks/000000/xxxxxxxxx')
        BOT.load_files()
        BOT.start_worker()
        time.sleep(1)
