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




class Crawler:
    COINS = ["ETH"] # Every coin to be Available to crawl so far
    HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
    # Parameters related to Etherium
    ETH_URL = "https://etherscan.io/txs" # Ehterscand Transcation URL
    ETH_TXS_CLASS_TAG = "myFnExpandBox_searchVal"
    ETH_METHOD = ['Repay', 'Borrow', 'Redeem', 'Underlying', 'Single', 'Transfer']


    def __init__(self) -> None:
        self.coin_users_map = {}
        for coin in self.COINS:
            self.coin_users_map[coin] = []
        for user in get_whitelist():
            user_coins = UserConfiguration(user).load_config()['coins']
            for coin in user_coins:
                self.coin_users_map[coin].append(user)
    

    def extract_txs(self, response_list: list, only_first=False, prev_first_hash: str=None) -> tuple:
        match = False
        data = []
        for response in response_list:
            soup = bs4.BeautifulSoup(response.content, "html.parser")
            table = soup.find('tbody', {'class':'align-middle text-nowrap'})
            for row in table.find_all('tr'):
                row_data = row.find_all('td')
                txs_hash = row_data[1].text.strip()
                txs_values = {
                    "hash": txs_hash,
                    "Method": row_data[2].text.strip(),
                    "Block": row_data[3].text.strip(),
                    "From": row_data[7].text.strip(),
                    "To": row_data[9].text.strip(),
                    "Value": row_data[10].text.strip(),
                    "Txn Fee": row_data[11].text.strip(),
                    "URL for detail": ospt.join(self.ETH_URL, txs_hash)
                }
                # print(">> ",txs_values['Method'])
                if only_first:
                    data.append(txs_values)
                    break
                elif txs_values['hash']==prev_first_hash:
                    match = True
                    break
                else:
                    if txs_values['Method'] in self.ETH_METHOD:
                        data.append(txs_values)
            if match:
                break
        # print(len(data))
        return (data, match)


    def check_response(self, response: requests.models.Response, expected_status=200) -> None:
        if response.status_code == expected_status:
            print("Success!!")
        else:
            print('Request failed with status code:', response.status_code)        


    def store_data_to_user(self, users: list, coin_data: list, coin: str) -> None:
        for user in users:
            configuration = UserConfiguration(user)
            configuration.Lock_update_coin_alerts(coin_data=coin_data, coin=coin)


    def crawl_store_ether(self, users: list) -> None:
        """
        Crawl etherium transaction from Etherscan site and Store the processed data to user's "alerts.json" file
        """
        coin = 'ETH'
        num_txs = 25
        num_page = 1
        request_num = 5

        # receive and process the first response
        while True:
            response = requests.get(self.ETH_URL+f"?ps={num_txs}&p={num_page}", headers=self.HEADERS)
            if response.status_code != 200: continue
            else:   break
        data, _ = self.extract_txs(response_list=[response], only_first=True)
        print(data) #<-----------------------------------------------
        prev_first_hash = data[0]['hash'] # set first transaction in first response html file

        num_txs = 100
        while True:
            # keep receiving the response
            response_list = []
            while len(response_list) < request_num:
                response = requests.get(self.ETH_URL+f"?ps={num_txs}&p={len(response_list)+1}", headers=self.HEADERS)
                if response.status_code == 200:
                    response_list.append(response)
            data, _ = self.extract_txs(response_list=response_list, only_first=False, prev_first_hash=prev_first_hash)
            if len(data) > 0:
                self.store_data_to_user(users=users, coin_data=data, coin=coin)
                prev_first_hash = data[0]['hash']
                print("change!!!") #<-----------------------------------------------
            else:
                print("not change...") #<-----------------------------------------------


    def main_process(self) -> None:
        for coin, users in self.coin_users_map.items():
            if coin == "ETH" and len(users) > 0:
                threading.Thread(target=self.crawl_store_ether, daemon=True, args=[users]).start()



    def run(self) -> None:
        restart_period = 10
        try:
            self.main_process()
        except KeyboardInterrupt:
            return
        except Exception as exc:
            logger.critical(f"An error has occurred in the mainloop - restarting in 5 seconds...", exc_info=exc)
            self.alert_admins(message=f"A critical error has occurred in the TaapiioProcess "
                                      f"(Restarting in {restart_period} seconds) - {exc}")
            sleep(restart_period)
            return self.run()