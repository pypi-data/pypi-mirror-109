import json
import time
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import requests

from .. import EthereumNetwork
from .contract_metadata import ContractMetadata


class EtherscanClientException(Exception):
    pass


class EtherscanClientConfigurationProblem(Exception):
    pass


class EtherscanRateLimitError(EtherscanClientException):
    pass


class EtherscanClient:
    NETWORK_WITH_URL = {
        EthereumNetwork.MAINNET: 'https://api.etherscan.io',
        EthereumNetwork.RINKEBY: 'https://api-rinkeby.etherscan.io',
        EthereumNetwork.BINANCE: 'https://api.bscscan.com',
    }

    def __init__(self, network: EthereumNetwork, api_key: Optional[str] = None):
        self.network = network
        self.api_key = api_key
        self.base_url = self.NETWORK_WITH_URL.get(network)
        if self.base_url is None:
            raise EtherscanClientConfigurationProblem(f'Network {network.name} - {network.value} not supported')
        self.http_session = requests.Session()

    def build_url(self, path: str):
        url = urljoin(self.base_url, path)
        if self.api_key:
            url += f'&apikey={self.api_key}'
        return url

    def _get_contract_abi(self, contract_address: str) -> Optional[Dict[str, Any]]:
        url = self.build_url(f'api?module=contract&action=getabi&address={contract_address}')
        response = self.http_session.get(url)

        if response.ok:
            response_json = response.json()
            result = response_json['result']
            if 'Max rate limit reached, please use API Key for higher rate limit' == result:
                raise EtherscanRateLimitError
            if response_json['status'] == '1':
                return json.loads(result)

    def get_contract_metadata(self, contract_address: str, retry: bool = True) -> Optional[ContractMetadata]:
        contract_abi = self.get_contract_abi(contract_address, retry=retry)
        if contract_abi:
            return ContractMetadata(None, contract_abi, False)

    def get_contract_abi(self, contract_address: str, retry: bool = True):
        for _ in range(3):
            try:
                return self._get_contract_abi(contract_address)
            except EtherscanRateLimitError as exc:
                if not retry:
                    raise exc
                else:
                    time.sleep(5)
