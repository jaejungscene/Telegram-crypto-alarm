from __init__ import *
from bot.crawler import *

class testCrawler:
    def __init__(self) -> None:
        pass

    @func_logger
    def extract_txs_TEST(self) -> None:
        PROXY = False
        testCrawler = Crawler()
        page = 1
        num_txs = 10 # 10, 25, 50, 100
        response = requests.get(ETH_URL+f"?ps={num_txs}&p={page}", headers=HEADERS)
        data, match = testCrawler.extract_txs([response], only_first=False, prev_first_hash=None)
        print(f"data: {data}")
        print(f"match: {match}")


if __name__ == "__main__":
    # test = testCrawler()
    # test.extract_txs_TEST() 

    def get_requests(url:str, **param):
        if len(param) == 0:
            print("param is empty")
        else:
            print(param)
    
    get_requests("asdf")
    get_requests("asdf", num_txs=1, num_page=32)


    # file = "./setApprovalForAll.html"
    # # file = "./TransferFile.html"
    # with open(file, "rb") as f:
    #     html = f.read()
    # import bs4
    # soup = bs4.BeautifulSoup(html, "html.parser")
    # result = soup.find(string=re.compile("Function: "))
    # if result is not None:
    #     print(re.split('\n| |\(', result.text)[1])
    # else:
    #     print("Transfer")