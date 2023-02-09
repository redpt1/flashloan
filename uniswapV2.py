# address:0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f
import csv

from eth_utils import keccak

import pandas as pd

# function signature
STEP_1 = '0x' + keccak(b'PairCreated(address,address,address,uint256)').hex()
STEP_2 = '0x' + keccak(b'Swap(address,uint256,uint256,uint256,uint256,address)').hex()

STEP_3_1 = '0x' + keccak(b'swap(uint256,uint256,address,bytes)').hex()[:8]
STEP_3_2_1 =  '0x' + keccak(b'transfer(address,uint256)').hex()[:8]
STEP_3_2_2 = '0x' + keccak(b'transferFrom(address,address,uint256)').hex()[:8]

# FLASH_1 = '0x' + keccak(b'Flash(address,address,uint256,uint256,uint256,uint256)').hex()


def search_uniswap():
    csv_reader = pd.read_csv('E:/dataset/logs.csv')
    # 查找全部对合约地址
    pair_contract_address = []
    for index, row in csv_reader.iterrows():
        if STEP_1 == row['topics'].split(',')[0]:
            raw_address = '0x' + row['data'][26:66]
            pair_contract_address.append(raw_address)

    # 根据对合约地址聚合
    csv_group_by = csv_reader.groupby('address')
    # 获取触发swap事件的tx hash
    emit_swap_tx_hash = []
    for tx, group in csv_group_by:
        if tx in pair_contract_address:
            for index, row in group.iterrows():
                # 如果触发了swap事件
                if row['topics'].split(',')[0] == STEP_2:
                    emit_swap_tx_hash.append(row['transaction_hash'])
        else:
            continue
    # 检查tx在调用对合约中swap函数时data是否大于0
    csv_reader_tx = pd.read_csv('E:/dataset/transactions.csv')
    for tx, row in csv_reader_tx.iterrows():
        if row['hash'] in emit_swap_tx_hash:
            if STEP_3_1 == row['input'][:10]:
                # 总长度减去data数据部分的偏移量（字节）如果不足64位（32字节）就不是，移除
                if len(row['input']) - (10 + 4 * 64) <= 64:
                    emit_swap_tx_hash.remove(row['hash'])

    #TODO 最后两步判断

if __name__ == '__main__':
    search_uniswap()
