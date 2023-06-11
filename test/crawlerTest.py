import requests
import bs4
import os.path as ospt
import re


COINS = ["ETH"] # Every coin to be Available to crawl so far
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
# Parameters related to Etherium
ETH_URL = "https://etherscan.io/txs" # Ehterscand Transcation URL
ETH_TXS_CLASS_TAG = "myFnExpandBox_searchVal"
ETH_IGNORE_METHOD = list(map(lambda x: x.lower(), ['stake', 'withdrawal', 'approve', 'transfer']))
coin = 'ETH'
num_txs = 25
num_page = 1
request_num = 3


def extract_txs(response_list: list, only_first=False, prev_first_hash: str=None) -> tuple:
        match = False
        data = []
        temp = False

        for response in response_list:
            soup = bs4.BeautifulSoup(response.content, "html.parser")
            table = soup.find('tbody', {'class':'align-middle text-nowrap'})
            if table == None:
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
                    match = True
                    return (data, match, temp)
                else:
                    if txs_values['Method'] not in ETH_IGNORE_METHOD:
                        response = requests.get(txs_values['URL for detail'], headers=HEADERS)
                        # response = requests.get("https://etherscan.io/tx/0xb78170e645dcfa78b0264e76df5619e807026fb31e997f38f8b894cd8ee43dd3", headers=HEADERS)
                        if response.status_code == 200:
                            # soup = bs4.BeautifulSoup(response.content, "html.parser")
                            # ERC_check = soup.find("div", text="ERC-20", class_="row mb-4")
                            # print(ERC_check.text)
                            # return (txs_values, match, True)
                            
                            soup = bs4.BeautifulSoup(response.content, "html.parser")
                            result = soup.find(string=re.compile('ERC-20 Tokens'))
                            if result is not None:
                                data.append(txs_values)
                                temp = True
                        else:
                            print("Fail")
        return (data, match, temp)


cnt = 1
while True:
    print("count > ", cnt)
    while True:
        response = requests.get(ETH_URL+f"?ps={num_txs}&p={num_page}", headers=HEADERS)
        if response.status_code != 200: continue
        else:   break
    data, match, temp = extract_txs(response_list=[response])
    if temp == True:
        print(data)
        break
    cnt += 1