import datetime as dt
from typing import Union


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
        self.date_format = "%Y-%m-%d"

    def generate_create_data(self) -> str:
        return f"{self.registered_at.strftime(self.date_format)};{self.description};{self.credit};{self.value};{self.balance}"

    def to_dict(self):
        return {
            "date": self.registered_at.strftime(self.date_format),
            "description": self.description,
            "value": self.value,
            "credit": self.credit,
            "balance": self.balance,
            "bank_id": self.bank_id,
            "createData": self.generate_create_data(),
        }
