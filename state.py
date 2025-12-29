from typing import TypedDict


class State(TypedDict):
    t: float
    u_n: float
    y_n: float
    r_n: float
    i_t: float
    y_t: float
    pi_t: float
    pi_e: float
