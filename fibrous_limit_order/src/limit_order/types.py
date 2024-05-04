from typing import List, Dict

class Parameter:
    def __init__(self, name: str, _type: str):
        self.name = name
        self.type = _type

class TypedDataTypes:
    def __init__(self, type_name: str, parameters: List[Dict[str, str]]):
        self.type_name = type_name
        self.parameters = [Parameter(param['name'], param['type']) for param in parameters]

    def __iter__(self):
        return iter(self.parameters)

types = {
    'StarkNetDomain': TypedDataTypes('StarkNetDomain', [
        {'name': 'name', 'type': 'felt'},
        {'name': 'version', 'type': 'felt'},
        {'name': 'chainId', 'type': 'felt'},
    ]),
    'Order': TypedDataTypes('Order', [
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
    ]),
    'u256': TypedDataTypes('u256', [
        {'name': 'low', 'type': 'felt'},
        {'name': 'high', 'type': 'felt'},
    ]),
}

class SignOrder:
    def __init__(
        self,
        signer: str,
        makerAsset: str,
        takerAsset: str,
        makerAmount: int, #uint256
        takerAmount: int, #uint256
        orderPrice: int, #uint256
        useSolver: bool,
        partialFill: bool,
        expiration: int,
        nonce: int = None
    ):
        self.signer = signer
        self.makerAsset = makerAsset
        self.takerAsset = takerAsset
        self.makerAmount = makerAmount
        self.takerAmount = takerAmount
        self.orderPrice = orderPrice
        self.useSolver = useSolver
        self.partialFill = partialFill
        self.expiration = expiration
        self.nonce = nonce

    def __getitem__(self, key):
        return getattr(self, key)
