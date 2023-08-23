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
import time
from datetime import datetime, timedelta


def string_transform(s:str) -> str:
    """
    Set Approval For All  -->  setApprovalForAll
    """
    temp = s.split(" ")
    newStr = ""
    for i in range(len(temp)):
        temp[i] = temp[i].lower()
        if i!=0:
            temp[i] = temp[i][0].upper() + temp[i][1:]
        newStr += temp[i]
    return newStr


def string_inverse_transform(input_string):
    transformed_string = re.sub(r'(?<!^)(?=[A-Z])', ' ', input_string)
    transformed_string = transformed_string[0].upper() + transformed_string[1:]
    return transformed_string


COINS = ["ETH"] # Every coin to be Available to crawl so far
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
# Parameters related to Etherium
ETH_URL = "https://etherscan.io/txs" # Ehterscand Transcation URL
ETH_TXS_CLASS_TAG = 'align-middle text-nowrap'
ETH_IGNORE_METHOD = list(map(string_transform, ['stake', 'withdrawal', 'approve', 'transfer']))
THRESHOLD = 100.0
PROXY_URL = "https://proxy.scrapeops.io/v1/"
PROXY_API_KEY = '9d7a8540-5274-4b50-bfb2-4365359afaeb'
PROXY = False



class Crawler:
    def __init__(self) -> None:
        self.coin_users_map = {}
        for coin in COINS:
            self.coin_users_map[coin] = []


    def get_requests(self, url: str, **param) -> requests.Response:
        if len(param) != 0:
            url = f"{url}?ps={param['num_txs']}&p={param['num_page']}"

        if PROXY == False:
            response = requests.get(url, headers=HEADERS)
        else:
            print("############################")
            response = requests.get(
                url=PROXY_URL,
                params={
                    'api_key': PROXY_API_KEY,
                    'url': url, 
                },
            )
        return response


    def extract_txs(self, response_list: list, users: list, coin: str, only_first=False, prev_first_hash: str=None) -> tuple:
        first_txs = None
        for response in response_list:
            soup = bs4.BeautifulSoup(response.content, "html.parser")
            table = soup.find('tbody', {'class':ETH_TXS_CLASS_TAG})
            if table == None:
                logger.warn('%% None type table occurs %%')
                continue
            for row in table.find_all('tr'):
                row_data = row.find_all('td')
                txs_hash = row_data[1].text.strip()
                txs_time = (datetime.strptime(row_data[4].text.strip(), "%Y-%m-%d %H:%M:%S") + timedelta(hours=9)).strftime("%p %I:%M")
                txs_values = {
                    "Hash": txs_hash,
                    "Time": txs_time,
                    "Method": row_data[2].text.strip(),
                    # "Block": row_data[3].text.strip(),
                    # "From": row_data[7].div.a['href'].split("/")[-1],
                    # "To": row_data[9].div.a['href'].split("/")[-1],
                    # "Value": row_data[10].text.strip(),
                    # "Txn Fee": row_data[11].text.strip(),
                    "URL": ospt.join(ETH_URL[:-1], txs_hash)
                }
                if first_txs is None:
                    first_txs = txs_values
                if only_first or txs_values['Hash'] == prev_first_hash:
                    print("----- only_first or txs_values['Hash'] == prev_first_hash")
                    break
                else:
                    if self.check_txs(txs_values):
                        self.store_txs_to_database(users=users, coin_data=[txs_values], coin=coin)
                if len(get_whitelist()) == 0:
                    print(">>> There is no users.")
                    break
            if len(get_whitelist()) == 0:
                break
        return first_txs['Hash']



    def check_txs(self, txs_values: dict) -> bool:
        # time.sleep(0.25)
        response = self.get_requests(txs_values["URL"])
        if response.status_code != 200:
            print(f"----- fail requesting from {txs_values['URL']}")
            return False # fail

        ########## Test Logic ###########
        # file = "./ApproveFile.html"
        # file = "./setApprovalForAll.html"
        # file = "./TransferFile.html"
        # with open(file, "rb") as f:
        #     response = f.read()
        # soup = bs4.BeautifulSoup(response, "html.parser")
        #################################

        soup = bs4.BeautifulSoup(response.content, "html.parser")
        methodResult = soup.find(string=re.compile("Function: "))
        methodResult = re.split('\n| |\(', methodResult.text)[1] if methodResult is not None else None
        if methodResult is None or methodResult in ETH_IGNORE_METHOD:
            print('----- Method false')
            return False # fail

        ERC_check = soup.find(string=re.compile('ERC-20 Tokens'))
        if ERC_check == None:
            print('----- ERC false')
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
            print("----- price_list false")
            return False # fail
        
        max_values = -1
        for elem in price_list:
            v = float(elem.text[2:-1].replace(",", ""))
            if v > THRESHOLD and v > max_values:
                max_values = v
        if max_values == -1:
            print('----- price false')
            return False # fail

        txs_values["Method"] = string_inverse_transform(methodResult)
        txs_values['Exchanged Max Values'] = max_values
        print(">>>>>>>>>>>>>>>>>  Pass check txs")
        return True



    def store_txs_to_database(self, users: list, coin_data: list, coin: str) -> None:
        for user in users:
            try:
                configuration = UserConfiguration(user)
                configuration.Lock_update_coin_alerts(coin_data=coin_data, coin=coin)
            except Exception as e:
                print(f"Jump the {user} from this error: {e}")



    def start_crawl_store_ether(self, users: list) -> None:
        """
        Crawl etherium transaction from Etherscan site and Store the processed data to user's "alerts.json" file
        """
        coin = 'ETH'
        num_txs = 25
        num_page = 1
        request_num = 3

        # receive and process the first response
        while True:
            response = self.get_requests(ETH_URL, num_txs=num_txs, num_page=num_page)
            # response = requests.get(ETH_URL+f"?ps={num_txs}&p={num_page}", headers=HEADERS)
            if response.status_code != 200: continue
            else:   break
        # set first transaction in first response html file
        prev_first_hash = self.extract_txs(response_list=[response], users=users, coin=coin, only_first=True)

        num_txs = 100
        while True and len(get_whitelist()) > 0:
            # keep receiving the response
            response_list = []
            while len(response_list) < request_num:
                response = self.get_requests(ETH_URL, num_txs=num_txs, num_page=len(response_list)+1)
                # response = requests.get(ETH_URL+f"?ps={num_txs}&p={len(response_list)+1}", headers=HEADERS)
                if response.status_code == 200:
                    response_list.append(response)
            prev_first_hash = self.extract_txs(response_list=response_list, users=users, coin=coin, only_first=False, prev_first_hash=prev_first_hash)

            # if len(data) > 0:
            #     self.store_txs_to_database(users=users, coin_data=data, coin=coin)
            #     prev_first_hash = data[0]['Hash']
            #     print(">>>>>>>>>> change!!!") #<-----------------------------------------------
            # else:
            #     print(">>>>>>>>>> not change...") #<-----------------------------------------------


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
                self.start_crawl_store_ether(users)
                # threading.Thread(target=self.crawl_store_ether, daemon=True, args=[users]).start()


    def run(self) -> None:
        logger.info(f'{type(self).__name__} started')
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