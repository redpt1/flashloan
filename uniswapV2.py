# address:0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f
import re

from eth_utils import keccak

import pandas as pd

# function signature
STEP_1 = '0x' + keccak(b'PairCreated(address,address,address,uint256)').hex()
STEP_2 = '0x' + keccak(b'Swap(address,uint256,uint256,uint256,uint256,address)').hex()

STEP_3_1 = '0x' + keccak(b'swap(uint256,uint256,address,bytes)').hex()[:8]
STEP_3_2_1 = '0x' + keccak(b'transfer(address,uint256)').hex()[:8]
STEP_3_2_2 = '0x' + keccak(b'transferFrom(address,address,uint256)').hex()[:8]


def search_uniswap():
    csv_reader = pd.read_csv('E:/dataset/logs.csv')
    # 查找全部对合约地址
    pair_contract_address = []
    for index, row in csv_reader.iterrows():
        if STEP_1 == str(row['topics']).split(',')[0]:
            raw_address = '0x' + row['data'][26:66]
            pair_contract_address.append(raw_address)
    # 去重
    pair_contract_address = list(set(pair_contract_address))
    # print(len(pair_contract_address))
    # 根据对合约地址聚合
    csv_group_by = csv_reader.groupby('address')
    # 获取触发swap事件的tx hash
    emit_swap_tx_hash = []
    for tx, group in csv_group_by:
        if tx in pair_contract_address:
            for index, row in group.iterrows():
                # 如果触发了Swap事件
                if row['topics'].split(',')[0] == STEP_2:
                    emit_swap_tx_hash.append(row['transaction_hash'])

    # 去重
    emit_swap_tx_hash = list(set(emit_swap_tx_hash))

    flash_loan_list = []
    # 检查tx是否调用了swap函数
    # 调用对合约中swap函数时data是否大于0
    csv_reader_tx = pd.read_csv('E:/dataset/traces.csv')
    csv_trace_group_by = csv_reader_tx.groupby('transaction_hash')
    for tx, group in csv_trace_group_by:
        if tx in emit_swap_tx_hash:
            flag = 0
            for index, row in group.iterrows():
                # 如果存在swap函数
                if str(row['input'])[:10] == STEP_3_1:
                    # 并且data字段大于0
                    if len(row['input']) > 10 + 64 * 4 and int(row['input'][10 + 64 * 4:], 16) != 0:
                        flag = 1

                # 检查是否存在transfer or transferFrom

                if str(row['input'])[:10] == STEP_3_2_1 and flag == 1:
                    if '0x' + row['input'][10 + 24:10 + 64] in pair_contract_address:
                        flag = 2

                if str(row['input'])[:10] == STEP_3_2_2 and flag == 1:
                    if '0x' + row['input'][10 + 64 + 24:10 + 64 * 2] in pair_contract_address:
                        flag = 2

            if flag == 2:
                flash_loan_list.append(tx)

    flash_loan_list = list(set(flash_loan_list))
    for ans in flash_loan_list:
        print(ans)

    print(len(flash_loan_list))


if __name__ == '__main__':
    search_uniswap()
