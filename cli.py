import argparse


def non_negative_int(value: str) -> int:
    try:
        int_value = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} is not an integer")

    if int_value < 0:
        raise argparse.ArgumentTypeError(f"{value} needs to be an integer ≥ 0")

    return int_value


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "t",
        help="number of times simulation runs (default 10)",
        nargs="?",
        type=non_negative_int,
        default=10,
    )
    parser.add_argument(
        "--params",
        "-p",
        help="csv file containing parameters (default: parameters_baseline.csv). Must be located in resources folder",
        default="parameters_baseline.csv",
    )
    parser.add_argument(
        "--shocks",
        "-s",
        help="csv file containing shocks (default: shocks_baseline.csv). Must be located in resources folder",
        default="shocks_baseline.csv",
    )
    return parser
