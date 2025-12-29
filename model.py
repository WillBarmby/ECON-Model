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


def apply_shocks(params: dict, shocks_t: pd.DataFrame):
    updated = params.copy()
    for _, shock in shocks_t.iterrows():
        parameter = shock["parameter"]
        operation = shock["operation"]
        value = shock["value"]

        if operation == "add":
            updated[parameter] += value
        elif operation == "mul":
            updated[parameter] *= value
        elif operation == "replace":
            updated[parameter] = value
        else:
            raise ValueError(f"unknown operations")
    return updated


def find_initial_state(params: dict) -> dict:
    pi_e_0 = params["pi_e_0"]
    u_n = calc_natural_unemp(params)
    y_n = calc_natural_output(params, u_n)
    r_n = calc_natural_rate(params=params, natural_output=y_n)
    y_t = calc_output(params=params, real_rate=r_n)
    pi_t = calc_inflation(
        params=params, expected_inflation=pi_e_0, output=y_t, natural_output=y_n
    )
    pi_e = anchored_expectations(pi_t)
    i_t = set_nominal_rate(
        params, real_rate=r_n, inflation=pi_t, output=y_n, natural_output=y_n
    )

    initial_state = {
        "t": 0,
        "u_n": u_n,
        "y_n": y_n,
        "r_n": r_n,
        "i_t": i_t,
        "y_t": y_t,
        "pi_t": pi_t,
        "pi_e": pi_e,
    }
    return initial_state


def step(params_t: dict, prev_state: dict) -> dict:

    u_n = calc_natural_unemp(params_t)
    y_n = calc_natural_output(params_t, u_n)
    r_n = calc_natural_rate(params=params_t, natural_output=y_n)
    r_t = calc_real_rate(
        nominal_rate=prev_state["i_t"], expected_inflation=prev_state["pi_e"]
    )
    y_t = calc_output(params=params_t, real_rate=r_t)
    pi_t = calc_inflation(
        params=params_t,
        expected_inflation=prev_state["pi_e"],
        output=y_t,
        natural_output=y_n,
    )
    pi_e = anchored_expectations(pi_t)
    i_t = set_nominal_rate(
        params_t, real_rate=r_n, inflation=pi_t, output=y_n, natural_output=y_n
    )

    state = {
        "t": prev_state["t"] + 1,
        "u_n": u_n,
        "y_n": y_n,
        "r_n": r_n,
        "i_t": i_t,
        "y_t": y_t,
        "pi_t": pi_t,
        "pi_e": pi_e,
    }
    return state
