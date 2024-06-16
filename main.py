import argparse
from typing import Any, Dict, List, Union
import toml
from models.coverflex import CoverflexBalance


def init_cli() -> argparse.ArgumentParser:
    """Initializes the command line parser interface."""
    parser = argparse.ArgumentParser(
        prog="Balance Manager Parser", description="Parser for multiple balance sources", epilog=""
    )
    # option that takes a value
    parser.add_argument("-b", "--bank", choices=["coverflex", "revolut"], required=True)
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
    parser = init_cli()
    args = parser.parse_args()

    print(f"balance file: {args.balance}")
    print(f"bank: {args.bank}")

    if args.bank == "coverflex":
        coverflex = CoverflexBalance(args.balance)
        print (coverflex.movements)


if __name__ == "__main__":
    main()
