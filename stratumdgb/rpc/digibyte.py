import requests


class DigiByteRPC:
    def __init__(self, config):
        self.config = config

        self.rpc_user = config.get("rpcuser")
        self.rpc_password = config.get("rpcpassword")
        self.rpc_port = config.get("rpcport")

        self.rpc_url = f"http://127.0.0.1:{self.rpc_port}"


    def rpc_call(self, method, params=None):
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
            self.rpc_url,
            auth=(self.rpc_user, self.rpc_password),
            json=payload,
            timeout=5,
        )

        response.raise_for_status()

        return response.json()["result"]


    def get_blockchain_info(self):
        return self.rpc_call("getblockchaininfo")


    def get_block_template(self):
        return self.rpc_call("getblocktemplate", [{"rules": ["segwit"]}])
