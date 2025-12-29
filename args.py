import argparse


def non_negative_int(value: str) -> int:
    try:
        int_value = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} is not an integer")

    if int_value < 0:
        raise argparse.ArgumentTypeError(f"{value} needs to be an integer ≥ 0")

    return int_value


parser = argparse.ArgumentParser()
parser.add_argument(
    "t", help="number of times simulation runs", type=non_negative_int, default=10
)

args = parser.parse_args()
