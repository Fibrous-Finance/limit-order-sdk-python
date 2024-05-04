import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
import aiohttp
from fibrous_limit_order import *


async def full_fill_order():
    limit_order = LimitOrder(RPC_URL)
    my_account = account(RPC_URL, ACCOUNT_PUBLIC_KEY, ACCOUNT_PRIVATE_KEY, '1')

    orders = await limit_order.get_orders({'maker_asset': '0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7'})
    fill_amount = 10000  # ETH makerAmount of order
    selected_order = orders.data[0]

    async with aiohttp.ClientSession() as session:
        async with session.get('https://graph.fibrous.finance/tokens') as tokens:
            tokens_data = await tokens.json()

    print(utils.order_to_human_readable(selected_order, tokens_data))

    fill_order_resp = await limit_order.fill_order(selected_order.order_hash, str(fill_amount))
    if fill_order_resp['status'] != 'success':
        print('Error message: ', fill_order_resp['message'])
        return
    
    fill_order_call_data = {
        'contractAddress':limit_order.default_contract_address,
        'entrypoint':'fillOrder',
        'calldata':fill_order_resp['data']
    }

    approve_call_data = await limit_order.approve_order_amount(selected_order.taker_asset, int(selected_order.taker_amount))
    call_data = [approve_call_data, fill_order_call_data]
    tx_hash = await my_account.execute_v1(call_data, auto_estimate = True)

    print(tx_hash)

def main():
    asyncio.run(full_fill_order())

if __name__ == '__main__':
    main()