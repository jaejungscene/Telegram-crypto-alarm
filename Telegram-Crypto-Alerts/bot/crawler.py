import requests
import bs4
import os.path as ospt
import json
from time import sleep
from .io_client import get_whitelist, UserConfiguration
from .custom_logger import logger
from .static_config import WHITELIST_ROOT
from collections import OrderedDict
import threading

COINS = ["ETH"] # Every coin to be Available to crawl so far
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
# Parameters related to Etherium
ETH_URL = "https://etherscan.io/txs" # Ehterscand Transcation URL
ETH_TXS_CLASS_TAG = "myFnExpandBox_searchVal"
ETH_IGNORE_METHOD = list(map(lambda x: x.lower(), ['stake', 'withdrawal', 'approve', 'transfer']))
print(ETH_IGNORE_METHOD)
"""

"""


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
            table = soup.find('tbody', {'class':'align-middle text-nowrap'})
            if table == None:
                logger.warn('%% None type table occurs %%')
                # print("---------------> response:", response)
                # print("---------------> table:", table)
                continue
            for row in table.find_all('tr'):
                row_data = row.find_all('td')
                txs_hash = row_data[1].text.strip()
                txs_values = {
                    "hash": txs_hash,
                    "Method": row_data[2].text.strip().lower(),
                    "Block": row_data[3].text.strip(),
                    "From": row_data[7].text.strip(),
                    "To": row_data[9].text.strip(),
                    "Value": row_data[10].text.strip(),
                    "Txn Fee": row_data[11].text.strip(),
                    "URL for detail": ospt.join(ETH_URL[:-1], txs_hash)
                }
                if only_first:
                    data.append(txs_values)
                    break
                elif txs_values['hash']==prev_first_hash:
                    # print(">>>>>>>>>>>>>>> prev_first_hash:", prev_first_hash)
                    # if only_first: data.append(txs_values) #<----------------------------------- for test
                    match = True
                    break
                else:
                    if txs_values['Method'] not in ETH_IGNORE_METHOD:
                        data.append(txs_values)
            if match:
                break
        # print(">>>>>>>>>>>>>>>>>>>>> len(data):",len(data))
        return (data, match)
    

    def analyse_each_txs(url: str):
        response = requests.get(url)
        if response.status_code == 200:
            soup = bs4.BeautifulSoup(response.content, "html.parser")
         


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
        # print('>>>>>>>>>>>>>>> first txs hash: ',data[0]['hash']) #<-----------------------------------------------
        # print('>>>>>>>>>>>>>>> first txs block: ',data[0]['Block']) #<-----------------------------------------------
        # self.store_data_to_user(users=users, coin_data=data, coin=coin) #<-------------------------------------
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
            # print("%"*100)
            cfg = UserConfiguration(user)
            try:
                cfg.reset_all_alerts()
            except FileNotFoundError:
                logger.warn("%% FileNotFoundError occur %%")
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