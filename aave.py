# trace the flash loan event
from eth_utils import keccak

import pandas as pd

# function signature
# Lend pool v1 function signature
PATTERN_1 = '0x' + keccak(b'FlashLoan(address,address,uint256,uint256,uint256,uint256)').hex()
# Lend pool v2
PATTERN_2 = '0x' + keccak(b'FlashLoan(address,address,address,uint256,uint256,uint16)').hex()
# Lend pool v3
PATTERN_3 = '0x' + keccak(b'FlashLoan(address,address,address,uint256,uint8,uint256,uint16)').hex()


def search_aave():
    csv_reader = pd.read_csv('E:/dataset/logs.csv')
    num_of_p1 = 0
    num_of_p2 = 0
    num_of_p3 = 0
    for index, row in csv_reader.iterrows():
        if PATTERN_1 == row['topics'].split(',')[0]:
            num_of_p1 += 1
            print(row)
        elif PATTERN_2 == row['topics'].split(',')[0]:
            num_of_p2 += 1
            print(row)
        elif PATTERN_3 == row['topics'].split(',')[0]:
            num_of_p3 += 1
            print(row)

    print("v1: %d, v2: %d, v3: %d, total: %d" % (num_of_p1, num_of_p2, num_of_p3, num_of_p1 + num_of_p2 + num_of_p3))


if __name__ == '__main__':
    search_aave()
