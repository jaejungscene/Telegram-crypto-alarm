# from os import getenv
# import os
# import re
# for key, value in os.environ.items():
#     L = re.findall("TELEGRAM", key)
#     if len(L) > 0: 
#         print(f"{key}   =   {value}")


# print(getenv('SHELL'))
# print(getenv("TELEGRAM_BOT_TOKEN"))


# myList=[True, True, True, True]
# print(all(myList))
# myList2=[True, True, True, False]
# print(all(myList2))
# myList3=[False, False, False, False]
# print(all(myList3))

# import requests
# tg_bot_token = "6264357965:AAH10GjcRl8iQ0sW1pavXDdAckvAMXE5Tpk"
# group_id = 
# requests.post(url=f'https://api.telegram.org/bot{tg_bot_token}/sendMessage',
#             params={'chat_id': group_id, 'text': header_str + post, "parse_mode": "HTML"})

# import os
# print(os.listdir(os.path.dirname(__file__)))
# print(os.path.isdir(__file__))
# print(os.path.isdir(os.path.dirname(__file__)))

# if True:
#     if True:
#         print(
# """ETH/USDT Moving Average (MA):
#   1 - 1d PERIOD=30 ABOVE 1000.0 AT 1881.926
#   2 - hello"""
#         )

# agg = {
#     'ETH': {123:'as', 'fd':3.1},
#     'BTC': {'price': 4214}
#     }

# generator = (len(v)==0 for v in agg.values())
# print(generator)
# for v in generator:
#     print(v)
# print("-----------")
# print(all(len(v)==0 for v in agg.values()))
# print(all([False, False]))

# post_str = ""
# for pair, agg in agg.items():
#     post_str = pair + "\n  " + str(agg)
#     print(post_str)


# from bot.crawler import Crawler

# crawler = Crawler()
# crawler.run()

# s = {"name": "jaejung"}
# print(next(iter(s.keys())))
# ETH_METHOD = ['Repay', 'Borrow', 'Redeem', 'Underlying', 'Single', 'Transfer']
# s = 'Borrow'
# s1 = 'Jaejung'
# if s in ETH_METHOD:
#     print(True)
# if s1 in ETH_METHOD:
#     print("s1 true")

# path = "/home/jaejung/private/Telegram-crypto-alarm/Telegram-Crypto-Alerts/bot/whitelist/1234/alerts.json"
# import json
# with open(path, "r") as f:
#     data = json.load(f)
# new_data = data.copy()
# new_data['ETH'] = {}
# print(len(data['ETH']))
# print(len(new_data['ETH']))

# print(ETH_METHOD.append(['hello']))
# print(ETH_METHOD + ['hello'])

# import time
# from bot.crawler import Crawler

# crawler = Crawler()
# crawler.run()
# while True:
#     time.sleep(1)
#     print("--------> still running")
# s = "asdfa"
# print(s[:-1])

# from ratelimit import limits, sleep_and_retry
# POLLING_PERIOD = 1

# @sleep_and_retry
# @limits(calls=1, period=POLLING_PERIOD)
# def poll_all_alerts() -> None:
#     print("-----> hello world")

# for _ in range(10):
#     poll_all_alerts()


s = "\n - <b>Hash</b>: {alert['hash']}\
\n - <b>Method</b>: {alert['Method']}\
\n - <b>Block</b>: {alert['Block']}\
\n - <b>From</b>: {alert['From']}\
\n - <b>To</b>: {alert['To']}\
\n - <b>Value</b>: {alert['Value']}\
\n - <b>Txn Fee</b>: {alert['Txn Fee']}\
\n - <b>URL for detail</b>: {alert['URL for detail']}"

"""
<table>\
\n - <tr> <td><b>Hash</b></td> <td>{alert['hash']}</td> </tr>\
\n - <tr> <td><b>Method</b></td> <td>{alert['Method']}</td> </tr>\
\n - <tr> <td><b>Block</b></td> <td>{alert['Block']}</td> </tr>\
\n - <tr> <td><b>From</b></td> <td>{alert['From']}</td> </tr>\
\n - <tr> <td><b>To</b></td> <td>{alert['To']}</td> </tr>\
\n - <tr> <td><b>Value</b></td> <td>{alert['Value']}</td> </tr>\
\n - <tr> <td><b>Txn Fee</b></td> <td>{alert['Txn Fee']}</td> </tr>\
\n - <tr> <td><b>URL for detail</b></td> {alert['URL for detail']}</td> </tr>\
</table>
"""

# L = ['asd', 're', 'qw']
# x = 'as'
# assert x in L, f"\'{x}\' coin is not available now, Please give me another coin"
# print("asldkjfs")

# from bot.io_client import UserConfiguration, get_whitelist
# print(get_whitelist())

# # UserConfiguration('123').whitelist_user(['ETH'])
# UserConfiguration('123').blacklist_user()
# L = [1]
# for i in L:
#     print("asdf")

x = "JAEJUjng"
print(x.lower())