import requests
import bs4
from time import sleep
from .io_client import get_whitelist, UserConfiguration
from .custom_logger import logger
from collections import OrderedDict


class Crawler:
    COINS = ["ETH"] # Every coin to be Available to crawl so far
    HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
    # Parameters related to Etherium
    ETH_URL = "https://etherscan.io/txs" # Ehterscand Transcation URL
    ETH_TXS_CLASS_TAG = "myFnExpandBox_searchVal"

    def __init__(self) -> None:
        self.coin_users_map = {}
        for coin in self.COINS:
            self.coin_users_map[coin] = []
        for user in get_whitelist():
            user_coins = UserConfiguration(user).load_config()['coins']
            for coin in user_coins:
                self.coin_users_map[coin].append(user)
    
    def extract_txs(response: requests.models.Response) -> dict:
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        table = soup.find('tbody', {'class':'align-middle text-nowrap'})
        data_dict = OrderedDict()
        for row in table.find_all('tr'):
            row_data = row.find_all('td')
            txs_hash = row_data[1].text.strip()
            txs_values = {
                "Method": row_data[2].text.strip(),
                "Block": row_data[3].text.strip(),
                "From": row_data[7].text.strip(),
                "To": row_data[9].text.strip(),
                "Value": row_data[10].text.strip(),
                "Txn Fee": row_data[11].text.strip()
            }
            data_dict[txs_hash] = txs_values
        return data_dict

    def crawl_store_ether(self, users) -> None:
        """
        Crawl etherium transaction from Etherscan site and Store the processed data to user's "alerts.json" file
        """
        num_txs = 100
        num_page = 1

        response = requests.get(self.ETH_URL+f"?ps={num_txs}&p={num_page}", headers=self.HEADERS)
        # process first response        
        data_dict = self.extract_txs(response)
        # set first transaction in first response html file
        self.prev_first_txs = next(iter(data_dict.keys()))


        if response.status_code == 200: print("Success!!")
        else:   print('Request failed with status code:', response.status_code)
        
        print(len(response.text))
        print("="*100)
        soup_data = bs4.BeautifulSoup(response.content, "html.parser")
        txs_box = soup_data.find_all(class_='align-middle text-nowrap')
        print(len(txs_box))
        # print(type(txs_box[0]))
        # print(txs_box[0].text[0:10])

        # print(len(response.content.decode('utf-8')))

        # if mem == response.text:
        #     print("same~~~~")
        # else:
        #     print("**Not Same**")
        #     with open("./temp0.html", "w") as f:
        #         f.write(mem)
        #     mem = response.text
        #     with open("./temp1.html", "w") as f:
        #         f.write(mem)
        sleep(1)

    def main_process(self) -> None:
        while True:
            for coin, users in self.coin_users_map.items():
                if coin == "ETH" and len(users) > 0:
                    self.crawl_store_ether(users)

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

            