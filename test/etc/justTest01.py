# from datetime import datetime, timedelta

# # Original string
# # original_string = "05:39:23"
# original_string = "Jun-11-2023 05:39:23 AM +UTC".split(" ")

# # Convert the string to a datetime object
# datetime_obj = datetime.strptime(original_string[0] + " " + original_string[1], "%b-%d-%Y %I:%M:%S") + timedelta(hours=9)
# print(datetime_obj)

# # Convert the datetime object to the desired format
# formatted_string = datetime_obj.strftime("%p %I:%M")

# print(formatted_string)  # Output: 오후 09:39
# print("-"*100)

# txs_time = (datetime.strptime("2023-06-24 13:23:11", "%Y-%m-%d %H:%M:%S") + timedelta(hours=9))
# print(txs_time)





# s = [1,2,3,4]
# condition = False
# v = 0
# while v < (len(s)):
#     print(s[v])
#     if s[v] == 3 and condition==False:
#         condition = True
#         continue
#     v += 1






# import logging

# logger = logging.getLogger(__name__)

# # Create a formatter with the desired time format
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# # Create a handler and set the formatter
# handler = logging.StreamHandler()
# handler.setFormatter(formatter)

# # Add the handler to the logger
# logger.addHandler(handler)

# # Set the logging level (e.g., DEBUG, INFO, WARNING, ERROR)
# logger.setLevel(logging.DEBUG)

# # Log a sample message
# logger.debug('This is a debug message')






import logging
import datetime

# Calculate the time adjustment
time_adjustment = datetime.timedelta(hours=4)
current_time = datetime.datetime.now()
adjusted_time = current_time + time_adjustment
time_format = adjusted_time.strftime('%Y-%m-%d %H:%M:%S')

logger = logging.getLogger(__name__)

# Create a formatter with the desired time format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt=time_format)

# Create a handler and set the formatter
handler = logging.StreamHandler()
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)

# Set the logging level (e.g., DEBUG, INFO, WARNING, ERROR)
logger.setLevel(logging.DEBUG)

# Log a sample message
logger.debug('This is a debug message')
