import re
import requests
import time
import random

def get_data():
    baseUrl = "https://phalcon.blocksec.com/tx/eth/"
    with open("uniswapV2.txt", "r") as f:
        ask_list = f.readlines()
    num = 0
    for i in ask_list:
        url = baseUrl + i.strip("\n")
        html = requests.post(url=url).text
        ans = re.findall("\"isFlashloan\":true", html)
        if len(ans) != 0:
            num += 1
            print(ans[0])
        else:
            print(i)
        time.sleep(random.uniform(0.5, 1))
    print(num)


if __name__ == "__main__":
    get_data()

