# trace the LogOperate → LogWithdraw → LogCall → LogDeposit event
from eth_utils import keccak

import pandas as pd

# function signature
STEP_1 = '0x' + keccak(b'LogOperation(address)').hex()
STEP_2 = '0x' + keccak(b'LogWithdraw(address,uint256,uint256,((bool,uint256),(bool,uint128)),address)').hex()
STEP_3 = '0x' + keccak(b'LogCall(address,uint256,address)').hex()
STEP_4 = '0x' + keccak(b'LogDeposit(address,uint256,uint256,((bool,uint256),(bool,uint128)),address)').hex()


def search_dydx():
    csv_reader = pd.read_csv('E:/dataset/logs.csv').groupby('transaction_hash')
    num_of_dydx = 0
    for tx, group in csv_reader:
        log_list = []
        for row in group['topics']:
            log_list.append(row.split(',')[0])
        if len(log_list) >= 4:
            if STEP_1 in log_list and STEP_2 in log_list and STEP_3 in log_list and STEP_4 in log_list:
                index_1 = log_list.index(STEP_1)
                index_2 = log_list.index(STEP_2)
                index_3 = log_list.index(STEP_3)
                index_4 = log_list.index(STEP_4)
                if index_1 < index_2 < index_3 < index_4:
                    num_of_dydx += 1
                    print(group)

    print("total: %d" % num_of_dydx)


if __name__ == '__main__':
    search_dydx()
