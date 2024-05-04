from typing import Optional, List
from starknet_py.net.models.typed_data import TypedData as TypedDataDict

class Order:
    def __init__(
        self,
        signer: str,
        maker_asset: str,
        taker_asset: str,
        maker_amount: str,
        taker_amount: str,
        order_price: str,
        expiration: int,
        use_solver: bool,
        partial_fill: bool,
        order_hash: Optional[str] = None,
        signature: Optional[List[str]] = None,
        **kwargs
        # remaining_maker_amount: Optional[str] = None,
        # remaining_taker_amount: Optional[str] = None,
        # id: Optional[int] = None,
        # nonce: Optional[int] = None,
        # status: Optional[str] = None,
        # is_inactive: Optional[bool] = None,
        # created_at: Optional[str] = None,
        # tx_hash: Optional[str] = None,
        # updated_at: Optional[str] = None
    ):
        self.signer = signer
        self.maker_asset = maker_asset
        self.taker_asset = taker_asset
        self.maker_amount = maker_amount
        self.taker_amount = taker_amount
        self.order_price = order_price
        self.expiration = expiration
        self.use_solver = use_solver
        self.partial_fill = partial_fill
        self.order_hash = order_hash
        self.signature = signature
        for key, value in kwargs.items():
            setattr(self, key, value)
        # self.remaining_maker_amount = remaining_maker_amount
        # self.remaining_taker_amount = remaining_taker_amount
        # self.id = id
        # self.nonce = nonce
        # self.status = status
        # self.is_inactive = is_inactive
        # self.created_at = created_at
        # self.tx_hash = tx_hash
        # self.updated_at = updated_at

class SupportedPairsResponse:
    def __init__(self, status: str, code: int, data: List[str]):
        self.status = status
        self.code = code
        self.data = data

class GetOrdersResponse:
    def __init__(self, status: str, code: int, data: List[Order]):
        self.status = status
        self.code = code
        self.data = data

class OrdersFilter:
    def __init__(
        self,
        walletAddress: Optional[str] = None,
        makerAsset: Optional[str] = None,
        takerAsset: Optional[str] = None,
        makerAmount: Optional[str] = None,
        takerAmount: Optional[str] = None,
        orderPrice: Optional[str] = None,
        page: Optional[int] = None,
        pageSize: Optional[int] = None
    ):
        self.walletAddress = walletAddress
        self.makerAsset = makerAsset
        self.takerAsset = takerAsset
        self.makerAmount = makerAmount
        self.takerAmount = takerAmount
        self.orderPrice = orderPrice
        self.page = page
        self.pageSize = pageSize

class NonceResponse:
    def __init__(self, status: str, code: int, data: int):
        self.status = status
        self.code = code
        self.data = data

class FillOrderResponse:
    def __init__(self, status: str, code: int, data: List[str]):
        self.status = status
        self.code = code
        self.data = data

class SignMessageResponse:
    def __init__(self, orderHash: str, typedData: TypedDataDict):
        self.orderHash = orderHash
        self.typedData = typedData

class PlaceOrderResponse:
    def __init__(self, status: str, code: int, data: Order):
        self.status = status
        self.code = code
        self.data = data
