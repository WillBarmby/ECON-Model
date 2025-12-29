from typing import TypedDict


class Params(TypedDict):
    m: float
    z: float
    alpha: float
    L: float

    c_0: float
    c_1: float
    b_0: float
    b_1: float
    b_2: float

    T: float
    G: float
    x: float

    pi_target: float
    phi_pi: float
    phi_y: float

    pi_e_0: float
