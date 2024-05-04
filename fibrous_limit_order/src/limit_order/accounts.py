from starknet_py.net.account.account import Account
from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.net.signer.stark_curve_signer import KeyPair

def account(node_url: str, public_key: str, private_key: str, is_cairo_1: str) -> Account:
    provider = FullNodeClient(node_url=node_url)
    account_instance = Account(client=provider, address=public_key, key_pair=KeyPair(private_key, public_key), chain=is_cairo_1)
    return account_instance
