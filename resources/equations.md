## Model Equations (Discrete Time)

### 1) Natural Unemployment and Natural Output
Natural unemployment:
$$
u_n = \frac{m + z}{\alpha}
$$

Natural output (employment times labor-force scale):
$$
Y_n = L(1-u_n)
$$

---

### 2) Output / IS (Goods Market)
Define the effective real rate faced by demand as:
$$
r^{\text{eff}}_t = r_t + x
$$

Output is:
$$
Y_t = \frac{c_0 - c_1 T + b_0 + G - b_2(r_t + x)}{1 - c_1 - b_1}
$$

Key multiplier:
$$
\frac{1}{1-c_1-b_1}
$$

---

### 3) Inflation / Phillips Curve
Inflation evolves via expected inflation plus an output-gap term:
$$
\pi_t = \pi^e_{t-1} + \alpha \cdot \frac{Y_t - Y_n}{L}
$$

---

### 4) Fisher Relation (Real Rate)
Real rate uses last period’s nominal rate and expected inflation:
$$
r_t = i_{t-1} - \pi^e_{t-1}
$$

---

### 5) Natural Real Rate
Natural real rate is the real rate that sets $Y_t = Y_n$ in the IS equation:
$$
r_n
= \frac{c_0 - c_1 T + b_0 + G - (1-c_1-b_1)Y_n}{b_2} - x
$$

---

### 6) Monetary Policy Rule (Taylor-style)
Nominal rate reacts to inflation and the output gap around natural output:
$$
i_t = r_n + \pi_t
      + \phi_\pi(\pi_t - \pi^*)
      + \phi_y\left(\frac{Y_t - Y_n}{Y_n}\right)
$$
where $\pi^* = \pi_{\text{target}}$.

---

### 7) Inflation Expectations
Expectation formation (fully adjusting / adaptive to realized inflation):
$$
\pi^e_t = \pi_t
$$

---

### 8) Timing / Update Order (per period $t$)
Given state at $t-1$ and parameters at $t$:
1. Compute $u_n, Y_n, r_n$ from current parameters.
2. Compute $r_t = i_{t-1} - \pi^e_{t-1}$.
3. Compute $Y_t$ from IS using $r_t$.
4. Compute $\pi_t$ from Phillips using $\pi^e_{t-1}$ and $Y_t - Y_n$.
5. Set $\pi^e_t = \pi_t$.
6. Set $i_t$ from the policy rule.

---

### 9) Shocks (Parameter Updates)
At time $t$, parameters may be updated by shock operations:
- add: $\theta \leftarrow \theta + v$
- mul: $\theta \leftarrow \theta \cdot v$
- replace: $\theta \leftarrow v$