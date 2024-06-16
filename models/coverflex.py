import os
import json
import datetime as dt
from typing import Dict, List, Union
from models.balance import Balance


class CoverflexBalance:
    def __init__(self, filepath: str, bank_id: Union[None, int]=None):
        self.filepath = filepath
        self.bank_id = bank_id
        self.movements: List[Balance] = []

        self.parse_json_file()

    def parse_datetime(self, balance_datetime: str) -> dt.datetime:
        return dt.datetime.strptime(balance_datetime, "%Y-%m-%dT%H:%M:%S.%fZ")

    def validate_fields(self, movement) -> bool:

        if "description" not in movement:
            return False

        if "is_debit" not in movement:
            return False

        if "executed_at" not in movement:
            return False

        if "amount" not in movement or "amount" not in movement["amount"]:
            return False

        if "balance_after" not in movement or "amount" not in movement["balance_after"]:
            return False

        return True

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
            if not self.validate_fields(movement):
                # TODO: log error
                continue

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
