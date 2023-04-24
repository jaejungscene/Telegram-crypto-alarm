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

agg = {
    'ETH': {123:'as', 'fd':3.1},
    'BTC': {'price': 4214}
    }

# generator = (len(v)==0 for v in agg.values())
# print(generator)
# for v in generator:
#     print(v)
# print("-----------")
# print(all(len(v)==0 for v in agg.values()))
# print(all([False, False]))

post_str = ""
for pair, agg in agg.items():
    post_str = pair + "\n  " + str(agg)
    print(post_str)