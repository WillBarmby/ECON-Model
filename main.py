from pathlib import Path
from config.paths import RESOURCES_DIR
from csv_reader import read_parameters, validate_params
from model import find_initial_state, apply_shocks, step
from params import Params
from state import State
import pandas as pd
import argparse


def non_negative_int(value: str) -> int:
    try:
        int_value = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} is not an integer")

    if int_value < 0:
        raise argparse.ArgumentTypeError(f"{value} needs to be an integer ≥ 0")

    return int_value


if __name__ == "__main__":

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
    args = parser.parse_args()
    params_file: Path = RESOURCES_DIR / args.params
    shocks_file: Path = RESOURCES_DIR / args.shocks
    if not params_file.exists():
        raise FileNotFoundError(f"No file found for params: {params_file}")
    if not shocks_file.exists():
        raise FileNotFoundError(f"No file found for shocks: {shocks_file}")

    raw_params = read_parameters(str(params_file))
    params: Params = validate_params(raw_params)

    t_sim = args.t
    df = pd.read_csv(str(shocks_file)).set_index("t")
    states: list[State] = []
    state = find_initial_state(params)
    states.append(state)
    for t in range(t_sim):
        shocks_t = df.loc[[t]] if t in df.index else pd.DataFrame()
        params_t = apply_shocks(params=params, shocks_t=shocks_t)

        state = step(params_t, prev_state=state)
        states.append(state)
        params = params_t
    df_final = pd.DataFrame(states).set_index("t")
    print(df_final)
