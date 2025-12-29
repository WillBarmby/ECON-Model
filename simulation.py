from pathlib import Path
from config.paths import RESOURCES_DIR
from csv_reader import read_parameters, validate_params
from model import find_initial_state, apply_shocks, step
from params import Params
from state import State
from cli import build_parser
import pandas as pd


def run_simulation(params: Params, shocks: pd.DataFrame, t_sim: int) -> pd.DataFrame:

    states: list[State] = []
    state = find_initial_state(params)
    states.append(state)

    for t in range(t_sim):
        shocks_t = shocks.loc[[t]] if t in shocks.index else pd.DataFrame()
        params_t = apply_shocks(params=params, shocks_t=shocks_t)
        state = step(params_t, prev_state=state)
        states.append(state)
        params = params_t

    return pd.DataFrame(states).set_index("t")
