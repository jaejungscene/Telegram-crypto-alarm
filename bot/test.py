import requests
import bs4
from selenium import webdriver
import time
from collections import OrderedDict

URL = "https://etherscan.io/txs"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
}
TXS_CLASS_TAG = "myFnExpandBox_searchVal"
num_txs = 100
num_page = 1
users = [1234, 5693094929]

def extract_txs_hash(response: requests.models.Response) -> str:
    soup = bs4.BeautifulSoup(response.content, "html.parser")
    txs_hashs = soup.find_all(class_=TXS_CLASS_TAG)
    print(len(txs_hashs))
    print(txs_hashs[0].text)
    proc_txs_hash = ""
    for h in txs_hashs:
        proc_txs_hash = proc_txs_hash + h.text + "\n"
    return proc_txs_hash

def extract_txs(response, first=True):
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

response = requests.get(URL+f"?ps={num_txs}&p={num_page}", headers=HEADERS)
data_dict = extract_txs(response)
prev_first_txs = next(iter(data_dict.keys()))

for user in users:
    

print("----------- finish -------------")    


# 1,2,3,7,9,10,11

# str_hash = extract_txs_hash(response)
# list_hash = str_hash.split("\n")[0:-1]


# buffer = ""

# start = time.time()
# for i in range(20):
    
#     response = requests.get(URL+f"?ps={num_txs}&p={num_page}", headers=HEADERS)
    
#     if response.status_code == 200: print("Success!!")
#     else:   print('Request failed with status code:', response.status_code)

#     # soup = bs4.BeautifulSoup(response.text, "html.parser")
#     # select_element = soup.find("select", {"name": "ctl00$ContentPlaceHolder1$ddlRecordsPerPage"})
#     # option_element = select_element.find("option", {"value": "100"})
#     # data = {
#     #     "__EVENTTARGET": select_element["name"],
#     #     "__EVENTARGUMENT": "",
#     #     "__LASTFOCUS": "",
#     #     "__VIEWSTATE": soup.find("input", {"name": "__VIEWSTATE"})["value"],
#     #     "__VIEWSTATEGENERATOR": soup.find("input", {"name": "__VIEWSTATEGENERATOR"})["value"],
#     #     "__EVENTVALIDATION": soup.find("input", {"name": "__EVENTVALIDATION"})["value"],
#     #     select_element["name"]: option_element["value"]
#     # }
#     # response = requests.post(URL, headers=headers, data=data)
    
#     # if response.status_code == 200: print("Success!!")
#     # else:   print('Request failed with status code:', response.status_code)

#     soup = bs4.BeautifulSoup(response.content, "html.parser")
#     txs_hash = soup.find_all(class_='myFnExpandBox_searchVal')
#     print(len(txs_hash))
#     data = ""
#     for hash in txs_hash:
#         data = data + hash.text + "\n"
#     with open(f"./temp/temp{i}.html", "w") as f:
#         f.write(data)

#     if buffer == data:
#         print("Same")
#     else:
#         print("Difference!!")
#         buffer = data
#     print("=================")
# print("Elapsed time: {:.2f} seconds".format(time.time() - start))
#     # txs_box = soup.find_all(class_='align-middle text-nowrap')
#     # print(len(txs_box))
#     # txs_proc = [x for x in txs_box[1].text.split('\n') if x.strip()]
#     # print(txs_proc)
#     # with open("./temp0.html", "w") as f:
#     #     f.write(txs_box[1].text)
    