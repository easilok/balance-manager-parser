import unittest
import datetime as dt
from models.balance import Balance


class BalanceModelTest(unittest.TestCase):
    def test_standard_dict(self):
        """
        Test if proper dict from values is generated
        """
        registered_at = dt.datetime.now()
        balance = Balance(
            description="desc", value=12.43, credit=False, bank_id=1, registered_at=registered_at, balance=1000.21
        )

        balance_dict = balance.to_dict()

        self.assertEqual(balance_dict["date"], registered_at.isoformat())
        self.assertEqual(balance_dict["description"], "desc")
        self.assertEqual(balance_dict["value"], 12.43)
        self.assertEqual(balance_dict["credit"], False)
        self.assertEqual(balance_dict["balance"], 1000.21)
        self.assertEqual(balance_dict["bank_id"], 1)
        self.assertEqual(balance_dict["createData"], f"{registered_at.isoformat()};desc;False;12.43;1000.21")
