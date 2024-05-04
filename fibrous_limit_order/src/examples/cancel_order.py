import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from starknet_py.net.client_models import Call
from limit_order.limit_order import LimitOrder
from limit_order.mock_data import RPC_URL, ACCOUNT_PRIVATE_KEY, ACCOUNT_PUBLIC_KEY
from limit_order.accounts import account

async def cancel_order():
    limit_order = LimitOrder(RPC_URL)
    nonce = await limit_order.get_nonce(ACCOUNT_PUBLIC_KEY)
    cancel_order_call_data: Call = await limit_order.cancel_order(nonce['data'])
    my_account = account(RPC_URL, ACCOUNT_PUBLIC_KEY, ACCOUNT_PRIVATE_KEY, '1')
    tx_hash = await my_account.execute_v1(cancel_order_call_data)
    print(f'tx_hash: {tx_hash}')

def main():
    asyncio.run(cancel_order())

if __name__ == '__main__':
    main()