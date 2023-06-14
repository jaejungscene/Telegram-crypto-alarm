import requests
import bs4
import os.path as ospt
import json
import re
from time import sleep
from .io_client import get_whitelist, UserConfiguration
from .custom_logger import logger
from .static_config import WHITELIST_ROOT
from collections import OrderedDict
import threading
from datetime import datetime, timedelta


COINS = ["ETH"] # Every coin to be Available to crawl so far
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
# Parameters related to Etherium
ETH_URL = "https://etherscan.io/txs" # Ehterscand Transcation URL
ETH_TXS_CLASS_TAG = 'align-middle text-nowrap'
ETH_IGNORE_METHOD = list(map(lambda x: x.lower(), ['stake', 'withdrawal', 'approve', 'transfer']))
PROXY_API_KEY = '9d7a8540-5274-4b50-bfb2-4365359afaeb'
PROXY = False


class Crawler:
    def __init__(self) -> None:
        self.coin_users_map = {}
        for coin in COINS:
            self.coin_users_map[coin] = []

    def extract_txs(self, response_list: list, only_first=False, prev_first_hash: str=None) -> tuple:
        match = False
        data = []
        for response in response_list:
            soup = bs4.BeautifulSoup(response.content, "html.parser")
            table = soup.find('tbody', {'class':ETH_TXS_CLASS_TAG})
            if table == None:
                logger.warn('%% None type table occurs %%')
                continue
            for row in table.find_all('tr'):
                row_data = row.find_all('td')
                txs_hash = row_data[1].text.strip()
                txs_values = {
                    "Hash": txs_hash,
                    "Method": row_data[2].text.strip().lower(),
                    "Block": row_data[3].text.strip(),
                    "From": row_data[7].text.strip(),
                    "To": row_data[9].text.strip(),
                    "Value": row_data[10].text.strip(),
                    "Txn Fee": row_data[11].text.strip(),
                    "URL": ospt.join(ETH_URL[:-1], txs_hash)
                }
                if only_first:
                    print("only_first")
                    data.append(txs_values)
                    break
                elif txs_values['Hash']==prev_first_hash:
                    print("txs_values['Hash'] == prev_first_hash")
                    match = True
                    return (data, match)
                else:
                    if txs_values['Method'] not in ETH_IGNORE_METHOD\
                    and self.check_this_txs(txs_values) == True:
                        data.append(txs_values)
        return (data, match)
         

    def check_this_txs(self, txs_values: dict) -> bool:
        threshold = 1000.0

        if PROXY == False:
            response = requests.get(txs_values["URL"], headers=HEADERS)
        else:
            response = requests.get(
                url='https://proxy.scrapeops.io/v1/',
                params={
                    'api_key': PROXY_API_KEY,
                    'url': txs_values["URL"], 
                },
            )
        if response.status_code != 200:
            print(f"fail requesting from {txs_values['URL']}")
            return False # fail
        
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        ERC_check = soup.find(string=re.compile('ERC-20 Tokens'))
        if ERC_check == None:
            print('> ERC false')
            return False # fail
        
        ERC_table = ERC_check.parent
        while True:
            try:
                if ERC_table["class"][0] == "row":
                    break
            except KeyError:
                pass
            ERC_table = ERC_table.parent
        price_list = ERC_table.find_all('span', class_="text-muted me-1")
        if len(price_list) == 0:
            print("> price_list false")
            return False # fail
        
        values = []
        for elem in price_list:
            v = float(elem.text[2:-1].replace(",", ""))
            if v < threshold:
                print('> price false')
                return False # fail
            values.append(v)
        
        time_string = soup.find('span', {"id":"showUtcLocalDate"})\
                    .text\
                    .split(" ")
        formatted_str = (datetime.strptime(time_string[0] + " " + time_string[1], "%b-%d-%Y %I:%M:%S") + timedelta(hours=9))\
                        .strftime("%p %I:%M")
        txs_values['time'] = formatted_str
        txs_values['values'] = values
        print(">>>>>>>>>>>>>>>>>  Pass check txs")
        return True
            
            
    def check_response(self, response: requests.models.Response, expected_status=200) -> None:
        if response.status_code == expected_status:
            print("Success!!")
        else:
            print('Request failed with status code:', response.status_code)        


    def store_data_to_user(self, users: list, coin_data: list, coin: str) -> None:
        for user in users:
            try:
                configuration = UserConfiguration(user)
                configuration.Lock_update_coin_alerts(coin_data=coin_data, coin=coin)
            except Exception:
                print(f"Jump the {user}")


    def crawl_store_ether(self, users: list) -> None:
        """
        Crawl etherium transaction from Etherscan site and Store the processed data to user's "alerts.json" file
        """
        coin = 'ETH'
        num_txs = 25
        num_page = 1
        request_num = 3

        # receive and process the first response
        while True:
            response = requests.get(ETH_URL+f"?ps={num_txs}&p={num_page}", headers=HEADERS)
            if response.status_code != 200: continue
            else:   break
        data, _ = self.extract_txs(response_list=[response], only_first=True)
        prev_first_hash = data[0]['hash'] # set first transaction in first response html file

        num_txs = 100
        while True and len(get_whitelist()) > 0:
            # keep receiving the response
            response_list = []
            while len(response_list) < request_num:
                response = requests.get(ETH_URL+f"?ps={num_txs}&p={len(response_list)+1}", headers=HEADERS)
                if response.status_code == 200:
                    response_list.append(response)
            data, _ = self.extract_txs(response_list=response_list, only_first=False, prev_first_hash=prev_first_hash)
            if len(data) > 0:
                self.store_data_to_user(users=users, coin_data=data, coin=coin)
                prev_first_hash = data[0]['hash']
                print(">>>>>>>>>> change!!!") #<-----------------------------------------------
            else:
                print(">>>>>>>>>> not change...") #<-----------------------------------------------


    def main_process(self) -> None:
        for coin in COINS:
            self.coin_users_map[coin] = []

        for user in get_whitelist():
            cfg = UserConfiguration(user)
            try:
                cfg.reset_all_alerts()
            except Exception as e:
                logger.warn(f"$$$ {e} $$$")
                continue
            user_cfg = cfg.load_config()
            user_coins = user_cfg['coins']
            for coin in user_coins:
                self.coin_users_map[coin].append(user)

        for coin, users in self.coin_users_map.items():
            if coin == "ETH" and len(users) > 0:
                self.crawl_store_ether(users)
                # threading.Thread(target=self.crawl_store_ether, daemon=True, args=[users]).start()



    def run(self) -> None:
        restart_period = 10
        try:
            while True:
                self.main_process()
        except KeyboardInterrupt:
            return
        except Exception as exc:
            logger.critical(f"An error has occurred in the mainloop - restarting in 5 seconds...", exc_info=exc)
            # self.alert_admins(message=f"A critical error has occurred in the TaapiioProcess "
            #                           f"(Restarting in {restart_period} seconds) - {exc}")
            sleep(restart_period)
            return self.run()