from config.paths import PARAMETERS
from csv_reader import read_csv
from model import run_static_simulation
import pandas as pd


if __name__ == "__main__":
    params = read_csv(str(PARAMETERS))
    t_sim = int(params["T_sim"])

    df = run_static_simulation(params=params, t_sim=t_sim)
    print(df)
