from config.paths import PARAMETERS
from csv_reader import read_csv
import pandas as pd


def calc_natural_unemp(params: dict):
    wage_markup = params["m"]
    labor_friction = params["z"]
    alpha = params["alpha"]
    return (wage_markup + labor_friction) / alpha


def calc_natural_output(params: dict, natural_unemp):
    labor_force = params["L"]
    return labor_force * (1 - natural_unemp)


def calc_output(params: dict, real_rate):
    c_0 = params["c_0"]
    c_1 = params["c_1"]
    b_0 = params["b_0"]
    b_1 = params["b_1"]
    b_2 = params["b_2"]
    taxes = params["T"]
    gov_spending = params["G"]
    risk_premium = params["x"]

    return (
        c_0 - c_1 * taxes + b_0 - b_2 * (real_rate + risk_premium) + gov_spending
    ) / (1 - c_1 - b_1)


def calc_inflation(params: dict, expected_inflation, output, natural_output):
    labor_force = params["L"]
    alpha = params["alpha"]

    return expected_inflation + alpha * (output - natural_output) / labor_force


def calc_real_rate(nominal_rate, expected_inflation):
    return nominal_rate - expected_inflation


def calc_natural_rate(params: dict, natural_output):
    c_0 = params["c_0"]
    c_1 = params["c_1"]

    b_0 = params["b_0"]
    b_1 = params["b_1"]
    b_2 = params["b_2"]

    taxes = params["T"]
    gov_spending = params["G"]
    risk_premium = params["x"]
    return (
        c_0 - c_1 * taxes + b_0 + gov_spending - (1 - c_1 - b_1) * natural_output
    ) / b_2 - risk_premium


def set_nominal_rate(params: dict, real_rate, inflation, output, natural_output):
    target_inflation = params["pi_target"]
    phi_pi = params["phi_pi"]
    phi_y = params["phi_y"]

    return (
        real_rate
        + inflation
        + phi_pi * (inflation - target_inflation)
        + phi_y * ((output - natural_output) / natural_output)
    )


def anchored_expectations(inflation):
    return inflation


if __name__ == "__main__":
    params = read_csv(str(PARAMETERS))

    t_sim = int(params["T_sim"])

    rows = []
    for t in range(t_sim):
        pi_e_0 = params["pi_e_0"]
        u_n = calc_natural_unemp(params)
        y_n = calc_natural_output(params, u_n)
        r_n = calc_natural_rate(params=params, natural_output=y_n)
        i_0 = r_n + params["pi_target"]
        r_t = calc_real_rate(nominal_rate=i_0, expected_inflation=pi_e_0)
        y_t = calc_output(params=params, real_rate=r_n)
        pi_t = calc_inflation(
            params=params, expected_inflation=pi_e_0, output=y_t, natural_output=y_t
        )
        pi_e = anchored_expectations(pi_t)
        i_t = set_nominal_rate(
            params, real_rate=r_n, inflation=pi_t, output=y_n, natural_output=y_n
        )

        rows.append(
            {
                "t": t,
                "u_n": u_n,
                "y_n": y_n,
                "r_n": r_n,
                "i_t": i_t,
                "y_t": y_t,
                "pi_t": pi_t,
                "pi_e": pi_e,
            }
        )

    df = pd.DataFrame(rows).set_index("t")
    print(df)
