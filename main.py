from config.paths import PARAMETERS, SHOCKS
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
    args = parser.parse_args()
    raw_params = read_parameters(str(PARAMETERS))
    params: Params = validate_params(raw_params)
    t_sim = args.t
    df = pd.read_csv(str(SHOCKS)).set_index("t")
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
