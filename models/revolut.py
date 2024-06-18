import os
import csv
import datetime as dt
from typing import Any, Dict, List
from models.balance import Balance


class RevolutBalance:
    def __init__(self, filepath: str, bank_id: int):
        self.filepath = filepath
        self.bank_id = bank_id
        self.movements: List[Dict[str, Any]] = []

        self.parse_csv_file()

    def parse_datetime(self, balance_datetime: str) -> dt.datetime:
        return dt.datetime.strptime(balance_datetime, "%Y-%m-%d %H:%M:%S")

    def validate_fields(self, movement) -> bool:
        if "description" not in movement:
            return False

        if "type" not in movement:
            return False

        if "started date" not in movement:
            return False

        if "amount" not in movement:
            return False

        if "balance" not in movement:
            return False

        return True

    def parse_csv_file(self) -> List[Dict]:
        if not os.path.isfile(self.filepath):
            raise ValueError(f"File {self.filepath} does not exist")

        movement_list = []

        with open(self.filepath) as balance_file:
            reader = csv.reader(balance_file)

            header = next(reader)
            for row in reader:
                movement = {}
                for index in range(len(header)):
                    movement[header[index].lower()] = row[index]
                movement_list.append(movement)

        self.movements.clear()

        for movement in movement_list:
            if not self.validate_fields(movement):
                # TODO: log error
                continue

            balance = Balance(
                description=movement["description"],
                value=float(movement["amount"]),
                credit=movement["type"] == "TOPUP",
                balance=float(movement["balance"]) if len(movement["balance"]) > 0 else 0,
                registered_at=self.parse_datetime(movement["started date"]),
                bank_id=self.bank_id,
            )

            self.movements.append(balance.to_dict())

        return self.movements
