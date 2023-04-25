import requests
import bs4
from selenium import webdriver
import time

APIKEY = "ZV44JZ963PVPZ2C2HQGW959BI4Q5581KM1"
# url = "https://api.etherscan.io/api\
# ?module=transaction\
# &action=getstatus\
# &txhash={}\
# &apikey={}".format(
#     "0xc5c97c3a7ab003dc540bdfa5f811631daadb51f3cb627746f1f12c98d83b0221", 
#     APIKEY
# )
url = "https://etherscan.io/txs"
# print(url)
# response = requests.get(url)
# print(response.status_code)
# soup_data = bs4.BeautifulSoup(response.content, "html.parser")
# print(
#     list(map(lambda x: x.get_text(), soup_data.find_all('title')))   
# )


from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Specify the path to the chromedriver executable
chromedriver_path = '/usr/bin/chromedriver'

# Create a new Service object with the chromedriver path
service = Service(executable_path=chromedriver_path)

# Create a new Chrome webdriver instance with the Service object
browser = webdriver.Chrome(service=service)
# browser = webdriver.Chrome('/usr/bin/chromedriver')
print("0"*100)
time.sleep(2)
browser.get(url)
print("1"*100)
time.sleep(2)
html = browser.page_source
print("2"*100)
time.sleep(2)
print(html)
print("3"*100)
time.sleep(2)
browser.close()


# username = 'jaejungscene'
# password = 'qw14785236!'
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
# }
# mem = ""
# while True:
#     response = requests.get(url, headers=headers)
#     if response.status_code == 200:
#         # Success
#         # print(response.text)
#         print("Success!!")
#     else:
#         # Failure
#         print('Request failed with status code:', response.status_code)
    
#     print(len(response.text))
#     print("="*100)
#     soup_data = bs4.BeautifulSoup(response.content, "html.parser")
#     print(soup_data.find_all(class_='dropdown-item active'))
#     # print(len(response.content.decode('utf-8')))
#     break
#     # if mem == response.text:
#     #     print("same~~~~")
#     # else:
#     #     print("**Not Same**")
#     #     with open("./temp0.html", "w") as f:
#     #         f.write(mem)
#     #     mem = response.text
#     #     with open("./temp1.html", "w") as f:
#     #         f.write(mem)
#     time.sleep(1)