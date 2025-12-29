from config.paths import PARAMETERS, SHOCKS
from csv_reader import read_parameters, read_shocks
from model import find_initial_state, apply_shocks, step
import pandas as pd


if __name__ == "__main__":
    params = read_parameters(str(PARAMETERS))
    t_sim = int(params["T_sim"])
    df = pd.read_csv(str(SHOCKS)).set_index("t")
    states = []
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
