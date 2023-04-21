# from os import getenv
# import os
# import re
# for key, value in os.environ.items():
#     L = re.findall("TELEGRAM", key)
#     if len(L) > 0: 
#         print(f"{key}   =   {value}")


# print(getenv('SHELL'))
# print(getenv("TELEGRAM_BOT_TOKEN"))


myList=[True, True, True, True]
print(all(myList))
myList2=[True, True, True, False]
print(all(myList2))
myList3=[False, False, False, False]
print(all(myList3))