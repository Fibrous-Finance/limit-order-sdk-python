import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from fibrous_limit_order import *


async def get_remaining_amount(orderHash):
    limit_order = LimitOrder(RPC_URL)
    remaining_amount = await limit_order.get_remaining_amount(orderHash)
    print(remaining_amount)
    return remaining_amount

def main():
    asyncio.run(get_remaining_amount('order_hash'))

if __name__ == '__main__':
    main()