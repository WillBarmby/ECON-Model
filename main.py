from pathlib import Path
from config.paths import RESOURCES_DIR
from csv_reader import read_parameters, validate_params
from model import find_initial_state, apply_shocks, step
from params import Params
from state import State
from cli import build_parser
from simulation import run_simulation
import pandas as pd

if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()
    t_sim = args.t

    params_file: Path = RESOURCES_DIR / args.params
    shocks_file: Path = RESOURCES_DIR / args.shocks
    if not params_file.exists():
        raise FileNotFoundError(f"No file found for params: {params_file}")
    if not shocks_file.exists():
        raise FileNotFoundError(f"No file found for shocks: {shocks_file}")

    raw_params = read_parameters(str(params_file))
    params: Params = validate_params(raw_params)

    shocks = pd.read_csv(str(shocks_file)).set_index("t")
    df_final = run_simulation(params=params, shocks=shocks, t_sim=t_sim)
    print(df_final)
