import sys
from os import path
root_path = path.dirname( path.dirname( path.abspath(__file__) ) )
sys.path.append(root_path)


def func_logger(function):
    def wrapper(*args, **kwargs):
        print("="*75)
        print(f"START: \'{function.__name__}\' function")
        print("-"*50)
        output = function(*args, **kwargs)
        print("-"*50)
        print(f"END: \'{function.__name__}\' function")
        print("="*75)
    return wrapper