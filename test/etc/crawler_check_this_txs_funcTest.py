import requests
import bs4
import re
from datetime import datetime, timedelta


# URL = "https://etherscan.io/tx/0xaea6720b767b6f7d38aab2aa36e170a268c82698ae6e02a250e8083bea4e0035"
URL = "https://etherscan.io/tx/0x8b4df28716f817f5dbaf2ed3373dd2a5b9f5eb5cd0b87e773b251381004a0c88"
PROXY_API_KEY = '9d7a8540-5274-4b50-bfb2-4365359afaeb'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}

def check_this_txs(txs_values: dict) -> bool:
    threshold = 1000.0

    # print(txs_values["URL"])
    response = requests.get(txs_values["URL"], headers=HEADERS)
    # response = requests.get(
    #     url='https://proxy.scrapeops.io/v1/',
    #     params={
    #         'api_key': PROXY_API_KEY,
    #         'url': txs_values["URL"], 
    #     },
    # )

    if response.status_code != 200:
        print('> status false')
        print(response.status_code)
        return False
    
    soup = bs4.BeautifulSoup(response.content, "html.parser")
    ERC_check = soup.find(string=re.compile('ERC-20 Tokens'))
    if ERC_check == None:
        print('> ERC false')
        return False
    
    # print(list(ERC_check.parent.parent.children)[1])
    # print(ERC_check.parent["class"])
    # print("--------------------")
    # print(ERC_check.parent.parent["class"])
    # print("--------------------")
    # print(ERC_check.parent.parent.parent["class"])

    ERC_table = ERC_check.parent
    while True:
        try:
            if ERC_table["class"][0] == "row":
                break
        except KeyError:
            pass
        ERC_table = ERC_table.parent
    print(ERC_table["class"])

    price_list = ERC_table.find_all('span', class_="text-muted me-1")
    if len(price_list) == 0:
        print("> price_list false")
        return False

    values = []
    for elem in price_list:
        v = float(elem.text[2:-1].replace(",", ""))
        if v < threshold:
            print('> price false')
            return False
        values.append(v)

    time_string = soup.find('span', {"id":"showUtcLocalDate"})\
                        .text\
                        .split(" ")
    formatted_str = (datetime.strptime(time_string[0] + " " + time_string[1], "%b-%d-%Y %I:%M:%S") + timedelta(hours=9))\
                    .strftime("%p %I:%M")

    txs_values['time'] = formatted_str
    txs_values['values'] = values
    print(txs_values)
    return True


txs_values = {'URL':URL}
if check_this_txs(txs_values) == True:
    print(txs_values)
    print('Pass')
else:
    print(txs_values)
    print("Fail")

# response = requests.get(URL, headers=HEADERS)
# if response.status_code == 200:
#     soup = bs4.BeautifulSoup(response.content, "html.parser")
#     ERC_check = soup.find(string=re.compile('ERC-20 Tokens'))
#     if ERC_check == None:
#         print("None")
#         exit()
#     print(type(ERC_check))
#     print("######"*10)
#     print(ERC_check)
#     print("######"*10)
#     price_list = list(ERC_check.parent.parent.parent.children)[1].find_all('span', class_="text-muted me-1")
#     for elem in price_list:
#         print(type(elem))
#         print(elem.text[2:-1])
#         if float(elem.text[2:-1].replace(",","")) > 5000.0:
#             print('Big')
#         else:
#             print("small..")
#         print("-----------")

#     print()
    # print(list(ERC_check.parent.parent.parent.children)[1])
    # print(len(list()))
    # ERC_check = re.search("ERC-20", soup.text)
    # print(ERC_check)
# else:
#     print("fail......!!!!!!!!!!!!")