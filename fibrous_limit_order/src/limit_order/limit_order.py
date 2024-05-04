import json
import aiohttp
from starknet_py.hash.selector import get_selector_from_name
from starknet_py.net.client_models import Call
from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.serialization._context import SerializationContext
from starknet_py.serialization.data_serializers import Uint256Serializer
from .constants import LIMIT_ORDER_API_URL, LIMIT_ORDER_CONTRACT_ADDRESS
from fibrous_limit_order.src.limit_order.order_types import Order, GetOrdersResponse, OrdersFilter, NonceResponse, SignMessageResponse, PlaceOrderResponse
from fibrous_limit_order.src.limit_order.message_sign import sign_message

class LimitOrder:
    _DEFAULT_API_URL = LIMIT_ORDER_API_URL
    _DEFAULT_CONTRACT_ADDRESS = LIMIT_ORDER_CONTRACT_ADDRESS

    def __init__(self, rpc_url=None, api_url=None):
        self.api_url = api_url or self._DEFAULT_API_URL
        self.rpc_url = rpc_url or ''

    @property
    def default_api_url(self):
        return self._DEFAULT_API_URL

    @property
    def default_contract_address(self):
        return self._DEFAULT_CONTRACT_ADDRESS

    async def get_nonce(self, walletAddress: str) -> NonceResponse:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.api_url}/nonce?walletAddress={walletAddress}") as response:
                return await response.json()

    async def get_remaining_amount(self, orderHash: str) -> str:
        provider = FullNodeClient(node_url=self.rpc_url)
        resp = await provider.call_contract(Call(
            to_addr= self.default_contract_address,
            selector= get_selector_from_name('remainingAmount'),
            calldata= [int(orderHash, 16)],
        ))

        remaining_amount = {
            'low': resp[0],
            'high': resp[1],
        }
        return str(remaining_amount)

    async def get_orders(self, filter: OrdersFilter = None) -> GetOrdersResponse:
        query_params = '&'.join([f"{key}={value}" for key, value in filter.items()]) if filter else ''
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.api_url}/orders?{query_params}") as response:
                data = await response.json()
                return GetOrdersResponse(
                    status=data.get('status', ''),
                    code=data.get('code', 0),
                    data=[Order(**order) for order in data.get('data', [])]
                )

    async def fill_order(self, orderHash, fill_amount=None):
        params = {'order_hash': orderHash}
        if fill_amount is not None:
            params['fill_amount'] = fill_amount

        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.api_url}/fillOrder", params=params, headers={'Content-Type': 'application/json'}) as response:
                data = await response.json()
                return data['data']

    async def sign_message(self, order: Order) -> SignMessageResponse:
    
        nonce_response = await self.get_nonce(order.signer)

        nonce = nonce_response['data'] + 1
        signed_message = sign_message(order, nonce)
        return signed_message

    async def place_order(self, order: Order) -> PlaceOrderResponse:
        data = json.dumps(vars(order))
        print(data)
        headers = {'Content-Type': 'application/json'}
        url = f"{self.api_url}/placeOrder"
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data, headers=headers) as response:
                return await response.json()

    async def approve_order_amount(self, token_address: str, amount: int) -> dict:
        #provider = FullNodeClient(node_url=self.rpc_url)
        approve_amount = list(Uint256Serializer().serialize_with_context(context=SerializationContext(), value = amount))
        return {
            'contractAddress': token_address,
            'entrypoint': 'approve',
            'calldata': [self.default_contract_address, hex(approve_amount[0]), hex(approve_amount[1])]
        }

    async def cancel_order(self, nonce: int) -> Call:
        return Call(
            to_addr=self.default_contract_address, # contractAddress
            selector=get_selector_from_name('cancelOrder'), # entrypoint
            calldata=[nonce] # calldata
        )
