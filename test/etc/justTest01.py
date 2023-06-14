from datetime import datetime, timedelta

# Original string
# original_string = "05:39:23"
original_string = "Jun-11-2023 05:39:23 AM +UTC".split(" ")

# Convert the string to a datetime object
datetime_obj = datetime.strptime(original_string[0] + " " + original_string[1], "%b-%d-%Y %I:%M:%S") + timedelta(hours=9)
print(datetime_obj)

# Convert the datetime object to the desired format
formatted_string = datetime_obj.strftime("%p %I:%M")

print(formatted_string)  # Output: 오후 09:39
print("-"*100)

txs_time = (datetime.strptime("2023-06-24 13:23:11", "%Y-%m-%d %H:%M:%S") + timedelta(hours=9))
print(txs_time)