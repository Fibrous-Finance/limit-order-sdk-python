from typing import Optional, Dict, Any, List
import time
from datetime import datetime

date_filter = Dict[str, Optional[int]]

def convert_unix_timestamp_to_date(unix_timestamp: int) -> str:
    date_time = datetime.utcfromtimestamp(unix_timestamp)
    return date_time.strftime('%Y-%m-%dT%H:%M:%S.000Z')

def order_to_human_readable(order: Any, tokens: List[Any]) -> Dict[str, Any]:
    maker_token = next((token for token in tokens if token['address'] == order.maker_asset), None)
    taker_token = next((token for token in tokens if token['address'] == order.taker_asset), None)

    maker_amount = float(order.maker_amount) / (10 ** maker_token['decimals'])
    taker_amount = float(order.taker_amount) / (10 ** taker_token['decimals'])
    maker_asset = maker_token['symbol']
    taker_asset = taker_token['symbol']
    order_price = float(order.order_price) / (10 ** taker_token['decimals'])
    remaining_taker_amount = float(order.remaining_taker_amount) / (10 ** taker_token['decimals'])
    remaining_maker_amount = float(order.remaining_maker_amount) / (10 ** maker_token['decimals'])
    expiration = convert_unix_timestamp_to_date(order.expiration)

    return {
        'signer': order.signer,
        'maker_asset': maker_asset,
        'taker_asset': taker_asset,
        'maker_amount': maker_amount,
        'taker_amount': taker_amount,
        'order_price': order_price,
        'remaining_maker_amount': remaining_maker_amount,
        'remaining_taker_amount': remaining_taker_amount,
        'expiration': expiration,
        'nonce': order.nonce,
        'use_solver': order.use_solver,
        'partial_fill': order.partial_fill,
        'order_hash': order.order_hash,
        'status': order.status,
        'signature': order.signature
    }
