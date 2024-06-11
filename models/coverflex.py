import os
import json
import datetime as dt
from typing import Dict, List, Union


class Balance:
    def __init__(
        self,
        description: str,
        value: float,
        credit: bool,
        bank_id: int,
        registered_at: dt.datetime,
        balance: Union[float, None] = None,
    ):
        self.description = description
        self.value = value
        self.credit = credit
        self.balance = balance
        self.bank_id = bank_id
        self.registered_at = registered_at

    def to_dict(self):
        return {
            "description": self.description,
            "value": self.value,
            "credit": self.credit,
            "balance": self.balance,
            "bank_id": self.bank_id,
            "date": self.registered_at.isoformat(),
        }


class CoverflexBalance:
    def __init__(self, filepath: str, bank_id=1):
        self.filepath = filepath
        self.bank_id = bank_id
        self.movements: List[Balance] = []

        self.parse_json_file()

    def parse_datetime(self, balance_datetime: str) -> dt.datetime:
        return dt.datetime.strptime(balance_datetime, "%Y-%m-%dT%H:%M:%S.%fZ")

    def parse_json_file(self) -> List[Dict]:
        if not os.path.isfile(self.filepath):
            raise ValueError(f"File {self.filepath} does not exist")

        parsed_json = {}

        with open(self.filepath) as balance_file:
            file_contents = balance_file.read()

            parsed_json = json.loads(file_contents)

        if "movements" not in parsed_json or "list" not in parsed_json["movements"]:
            raise ValueError("Parsed balance has unexpected data structure")

        movement_list = parsed_json["movements"]["list"]

        self.movements.clear()

        for movement in movement_list:
            # TODO: validate field existence

            balance = Balance(
                description=movement["description"],
                value=movement["amount"]["amount"] / 100,
                credit=not movement["is_debit"],
                balance=movement["balance_after"]["amount"] / 100,
                registered_at=self.parse_datetime(movement["executed_at"]),
                bank_id=self.bank_id,
            )

            self.movements.append(balance.to_dict())

        return self.movements
