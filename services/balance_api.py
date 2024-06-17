from typing import Dict, List, Union
import requests

from models.balance import Balance

DEFAULT_BALANCE_API_ENDPOINT = "http://localhost:8765"
DEFAULT_BALANCE_API_TOKEN = "TEST_API_TOKEN"


class BalanceAPI:
    def __init__(self, config: Union[None, Dict[str, str]]):
        self.url = DEFAULT_BALANCE_API_ENDPOINT
        self.token = DEFAULT_BALANCE_API_TOKEN

        if config is not None and "url" in config:
            self.url = config["url"]

        if config is not None and "token" in config:
            self.token = config["token"]

        self.headers = {"user-agent": "balance-manager-parser/0.0.1", "Authorization": f"Bearer {self.token}"}

    def bulk_create_balances(self, movements: List[Balance]) -> Union[None, requests.Response]:
        try:
            response = requests.post(
                url=f"{self.url}/api/v1/balance", headers=self.headers, json={"movements": movements}
            )

            return response
        except BaseException as exc:
            print(exc)
            return None
