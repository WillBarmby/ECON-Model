from config.paths import PARAMETERS
from csv_reader import read_csv
import pandas as pd


def calc_natural_unemp(wage_markup, labor_friction, alpha):
    return (wage_markup + labor_friction) / alpha


def calc_natural_output(u_n, labor_force):
    return labor_force * (1 - u_n)


def calc_output(c_0, c_1, taxes, b_0, b_1, b_2, r_t, x_t, gov_spending):
    return (c_0 - c_1 * taxes + b_0 - b_2 * (r_t + x_t) + gov_spending) / (
        1 - c_1 - b_1
    )


def calc_inflation(pi_e_t, alpha, y_t, y_n, labor_force):
    return pi_e_t + alpha * (y_t - y_n) / labor_force


def calc_real_rate(nominal_rate, expected_inflation):
    return nominal_rate - expected_inflation


def calc_natural_rate(c_0, c_1, taxes, b_0, b_1, b_2, x_t, gov_spending, y_n):
    return (c_0 - c_1 * taxes + b_0 + gov_spending - (1 - c_1 - b_1) * y_n) / b_2 - x_t


def set_nominal_rate(r_n, pi_t, pi_target, phi_pi, phi_y, y_t, y_n):
    return r_n + pi_t + phi_pi * (pi_t - pi_target) + phi_y * ((y_t - y_n) / y_n)


def anchored_expectations(pi_t):
    return pi_t


if __name__ == "__main__":
    params = read_csv(str(PARAMETERS))

    t_sim = int(params["T_sim"])

    c_0 = params["c_0"]
    c_1 = params["c_1"]

    b_0 = params["b_0"]
    b_1 = params["b_1"]
    b_2 = params["b_2"]

    taxes = params["T"]
    gov_spending = params["G"]
    risk_premium = params["x"]

    labor_force = params["L"]
    wage_markup = params["m"]
    labor_friction = params["z"]

    alpha = params["alpha"]

    pi_target = params["pi_target"]
    pi_0 = pi_target
    pi_e_0 = params["pi_e_0"]

    phi_pi = params["phi_pi"]
    phi_y = params["phi_y"]

    u_n = calc_natural_unemp(wage_markup, labor_friction, alpha)
    y_n = calc_natural_output(u_n, labor_force)

    r_n = calc_natural_rate(
        c_0, c_1, taxes, b_0, b_1, b_2, risk_premium, gov_spending, y_n
    )

    i_t = set_nominal_rate(r_n, pi_0, pi_target, phi_pi, phi_y, y_n, y_n)

    y_t = calc_output(
        c_0=c_0,
        c_1=c_1,
        taxes=taxes,
        b_0=b_0,
        b_1=b_1,
        b_2=b_2,
        r_t=r_n,
        x_t=risk_premium,
        gov_spending=gov_spending,
    )

    pi_t = calc_inflation(
        pi_e_t=pi_e_0, alpha=alpha, y_t=y_t, y_n=y_n, labor_force=labor_force
    )

    pi_e = anchored_expectations(pi_t)

    rows = []
    for t in range(t_sim):
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
