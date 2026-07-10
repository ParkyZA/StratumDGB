import requests

RPC_URL = "http://127.0.0.1:14022"
RPC_USER = "dgbminer"
RPC_PASSWORD = "ChooseAStrongPasswordHere"


def rpc_call(method, params=None):
    """
    Send a JSON-RPC request to DigiByte Core.
    """

    if params is None:
        params = []

    payload = {
        "jsonrpc": "1.0",
        "id": "stratumdgb",
        "method": method,
        "params": params,
    }

    response = requests.post(
        RPC_URL,
        auth=(RPC_USER, RPC_PASSWORD),
        json=payload,
        timeout=5,
    )

    response.raise_for_status()

    return response.json()["result"]


def get_blockchain_info():
    return rpc_call("getblockchaininfo")


def get_block_template():
    return rpc_call("getblocktemplate", [{"rules": ["segwit"]}])
