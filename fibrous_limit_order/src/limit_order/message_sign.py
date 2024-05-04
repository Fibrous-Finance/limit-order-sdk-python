from starknet_py.utils.typed_data import TypedData
from starknet_py.net.models.typed_data import StarkNetDomain
from .types import SignOrder, types
from fibrous_limit_order.src.limit_order.order_types import Order, SignMessageResponse

CHAINID = '0x534e5f474f45524c49'

def get_domain(chain_id: str) -> StarkNetDomain:
    return {
        'name': 'Fibrous Finance',
        'version': '1',
        'chainId': chain_id,
    }

def get_typed_data_hash(my_struct: SignOrder, chain_id: str, owner: str) -> str:
    _get_typed_data = get_typed_data(my_struct, chain_id)
    return TypedData.message_hash(_get_typed_data, int(owner, 16))

def get_typed_data(my_struct: SignOrder, chain_id: str) -> TypedData:
    return TypedData(
        types=types,
        primary_type='Order',
        domain=get_domain(chain_id),
        message=my_struct
    )

def sign_message(order: Order, nonce: int) -> SignMessageResponse:
    order_struct = SignOrder(
        signer=order.signer,
        makerAsset=order.maker_asset,
        takerAsset=order.taker_asset,
        makerAmount=order.maker_amount,  #uint256.bn_to_uint256(order['makerAmount']),
        takerAmount=order.taker_amount,  #uint256.bn_to_uint256(order['takerAmount']),
        orderPrice=order.order_price,   #uint256.bn_to_uint256(order['orderPrice']),
        useSolver=order.use_solver,
        partialFill=order.partial_fill,
        expiration=order.expiration,
        nonce=nonce,
    )

    typed_data_validate : TypedData = {
		'types': {
            'StarkNetDomain': [
                {'name': 'name', 'type': 'felt'},
                {'name': 'version', 'type': 'felt'},
                {'name': 'chainId', 'type': 'felt'},
            ],
            'Order': [
                {'name': 'signer', 'type': 'ContractAddress'},
                {'name': 'makerAsset', 'type': 'ContractAddress'},
                {'name': 'takerAsset', 'type': 'ContractAddress'},
                {'name': 'makerAmount', 'type': 'u256'},
                {'name': 'takerAmount', 'type': 'u256'},
                {'name': 'orderPrice', 'type': 'u256'},
                {'name': 'useSolver', 'type': 'bool'},
                {'name': 'partialFill', 'type': 'bool'},
                {'name': 'expiration', 'type': 'u64'},
                {'name': 'nonce', 'type': 'u64'},
            ],
            'u256': [
                {'name': 'low', 'type': 'felt'},
                {'name': 'high', 'type': 'felt'},
            ],
        },

		"primaryType": 'Order',

		'domain': {
            'name': 'Fibrous Finance',
            'version': '1',
            'chainId': CHAINID,
        },

		"message": {
            'signer': order.signer,
            'makerAsset': order.maker_asset,
            'takerAsset': order.taker_asset,
            'makerAmount': order.maker_amount,
            'takerAmount': order.taker_amount,
            'orderPrice': order.order_price,
            'useSolver': order.use_solver,
            'partialFill': order.partial_fill,
            'expiration': order.expiration,
            'nonce': nonce, 
        }
	}

    typed_data_hash = get_typed_data_hash(order_struct, CHAINID, order.signer)

    return SignMessageResponse(orderHash=typed_data_hash, typedData=typed_data_validate)
