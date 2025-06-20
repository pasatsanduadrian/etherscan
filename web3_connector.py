"""Minimal Web3 connector used by vesting logic."""

import os
import json
from typing import Any, Dict, List, Optional

import requests
from web3 import Web3
from dotenv import load_dotenv


class Web3Connector:
    """Utility class to interact with Ethereum networks via Infura."""

    INFURA_NETWORKS = {
        "mainnet": "https://mainnet.infura.io/v3/{project_id}",
        "goerli": "https://goerli.infura.io/v3/{project_id}",
        "polygon": "https://polygon-mainnet.infura.io/v3/{project_id}",
    }

    ETHERSCAN_APIS = {
        "mainnet": "https://api.etherscan.io/api",
        "goerli": "https://api-goerli.etherscan.io/api",
        "polygon": "https://api.polygonscan.com/api",
    }

    def __init__(self, network: str = "mainnet") -> None:
        load_dotenv()
        self.network = network.lower()
        project_id = os.getenv("INFURA_PROJECT_ID")
        if not project_id:
            raise EnvironmentError("INFURA_PROJECT_ID not set")
        if self.network not in self.INFURA_NETWORKS:
            raise ValueError(f"Unsupported network: {network}")

        self.infura_url = self.INFURA_NETWORKS[self.network].format(project_id=project_id)
        self.etherscan_key = os.getenv("ETHERSCAN_API_KEY")
        self.etherscan_url = self.ETHERSCAN_APIS[self.network]
        self.w3 = Web3(Web3.HTTPProvider(self.infura_url))

    # ------------------------------------------------------------------
    def _fetch_abi(self, address: str) -> Optional[List[Dict[str, Any]]]:
        if not self.etherscan_key:
            raise EnvironmentError("ETHERSCAN_API_KEY not set")
        params = {
            "module": "contract",
            "action": "getabi",
            "address": address,
            "apikey": self.etherscan_key,
        }
        try:
            resp = requests.get(self.etherscan_url, params=params, timeout=10)
            data = resp.json()
            if data.get("status") == "1":
                return json.loads(data["result"])
        except Exception:
            pass
        return None

    def _get_functions(self, abi: List[Dict[str, Any]]) -> List[str]:
        return [i.get("name", "") for i in abi if i.get("type") == "function"]

    def _call_contract_function(self, contract, func_name: str, address: str = None) -> Any:
        if not hasattr(contract.functions, func_name):
            return None
        func = getattr(contract.functions, func_name)
        try:
            return func().call()
        except Exception:
            if address:
                try:
                    return func(address).call()
                except Exception:
                    return None
            return None

    # ------------------------------------------------------------------
    def get_vesting_data(self, address: str) -> Dict[str, Any]:
        """Retrieve basic vesting information for a contract."""
        abi = self._fetch_abi(address)
        if not abi:
            raise ValueError("Unable to fetch contract ABI")

        checksum = Web3.to_checksum_address(address)
        contract = self.w3.eth.contract(address=checksum, abi=abi)
        functions = self._get_functions(abi)

        vested = 0
        released = 0
        if "vestedAmount" in functions:
            value = self._call_contract_function(contract, "vestedAmount", checksum)
            if value is not None:
                vested = float(value) / 1e18
        if "released" in functions:
            value = self._call_contract_function(contract, "released", checksum)
            if value is not None:
                released = float(value) / 1e18

        return {"vested": vested, "released": released, "functions": functions}

