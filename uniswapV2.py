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
    csv_reader = pd.read_csv('logs.csv')
    
    # Find all pairs of contract addresses
    pair_contract_address = []
    for index, row in csv_reader.iterrows():
        if STEP_1 == str(row['topics']).split(',')[0]:
            raw_address = '0x' + row['data'][26:66]
            pair_contract_address.append(raw_address)
            
    # Deduplicate
    pair_contract_address = list(set(pair_contract_address))
    
    # print(len(pair_contract_address))
    # According to the pair contract address to groupby
    csv_group_by = csv_reader.groupby('address')
    
    # Get the tx hash that triggers the swap event
    emit_swap_tx_hash = []
    for tx, group in csv_group_by:
        if tx in pair_contract_address:
            for index, row in group.iterrows():
                
                # If the Swap event is triggered
                if row['topics'].split(',')[0] == STEP_2:
                    emit_swap_tx_hash.append(row['transaction_hash'])

    # Deduplicate
    emit_swap_tx_hash = list(set(emit_swap_tx_hash))

    flash_loan_list = []
    
    # Check whether tx calls the swap function
    # Whether data is greater than 0 when calling the swap function in the pair contract
    csv_reader_tx = pd.read_csv('traces.csv')
    csv_trace_group_by = csv_reader_tx.groupby('transaction_hash')
    for tx, group in csv_trace_group_by:
        if tx in emit_swap_tx_hash:
            flag = 0
            for index, row in group.iterrows():
                
                # If there is a swap function
                if str(row['input'])[:10] == STEP_3_1:
                    
                    # And the data field is greater than 0
                    if len(row['input']) > 10 + 64 * 4 and int(row['input'][10 + 64 * 4:], 16) != 0:
                        flag = 1

                # Check if transfer or transferFrom exists
                if str(row['input'])[:10] == STEP_3_2_1 and flag == 1:
                    if '0x' + row['input'][10 + 24:10 + 64] in pair_contract_address:
                        flag = 2

                if str(row['input'])[:10] == STEP_3_2_2 and flag == 1:
                    if '0x' + row['input'][10 + 64 + 24:10 + 64 * 2] in pair_contract_address:
                        flag = 2

            if flag == 2:
                flash_loan_list.append(tx)

    flash_loan_list = list(set(flash_loan_list))

    f = open('uniswapV2.txt', 'w')
    for ans in flash_loan_list:
        f.write(ans+"\n")
    f.close()

    print(len(flash_loan_list))


if __name__ == '__main__':
    search_uniswap()
