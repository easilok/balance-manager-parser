import argparse
from typing import Any, Dict, List, Union
import toml
from models.coverflex import CoverflexBalance
from models.revolut import RevolutBalance
from services.balance_api import BalanceAPI


def init_cli(bank_names: List[str]) -> argparse.ArgumentParser:
    """Initializes the command line parser interface."""
    parser = argparse.ArgumentParser(
        prog="Balance Manager Parser", description="Parser for multiple balance sources", epilog=""
    )
    # option that takes a value
    parser.add_argument("-b", "--bank", choices=bank_names, required=True)
    # positional argument
    parser.add_argument("balance")

    return parser


def load_config(filepath="config.toml") -> Union[None, Dict[str, Any]]:
    config = None
    try:
        with open(filepath, "r") as f:
            config = toml.load(f)
    except BaseException:
        pass

    return config


def main():
    bank_names = []

    config = load_config()
    if config is not None and "banks" in config:
        bank_names = list(config["banks"])

    parser = init_cli(bank_names)
    args = parser.parse_args()

    print(f"balance file: {args.balance}")
    print(f"bank: {args.bank}")

    if args.bank == "coverflex":
        bank_id = config["banks"]["coverflex"] if config is not None else None
        coverflex = CoverflexBalance(args.balance, bank_id)
        print(coverflex.movements)
        balance_api = BalanceAPI(config["api"] if config is not None else None)
        response = balance_api.bulk_create_balances(coverflex.movements)
        print(response)
    elif args.bank == "revolut":
        bank_id = config["banks"]["revolut"] if config is not None else None
        revolut = RevolutBalance(args.balance, bank_id)
        print(revolut.movements)
        balance_api = BalanceAPI(config["api"] if config is not None else None)
        response = balance_api.bulk_create_balances(revolut.movements)
        print(response)


if __name__ == "__main__":
    main()
