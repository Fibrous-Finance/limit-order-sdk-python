import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from fibrous_limit_order import *

async def fill_order(orderHash, fill_amount=None):
    limit_order = LimitOrder()
    response = await limit_order.fill_order(orderHash, fill_amount)
    print(response)
    return response

FILL_AMOUNT = str(1000000000000000000)

def main():
    asyncio.run(fill_order('orderHash', FILL_AMOUNT))

if __name__ == '__main__':
    main()