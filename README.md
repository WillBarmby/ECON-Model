# IS–LM–PC Simulator
## What This Is

This is a simple, discrete-time simulator of the IS–LM–PC model of a closed macroeconomy. The program takes a set of structural parameters and a shock schedule for those parameters, and returns the **time path** of key macroeconomic variables over a specified number of periods.

The goal is clarity and experimentation rather than structural estimation — the model is transparent, modular, and intended to make counterfactual policy dynamics easy to explore.

## Model Specifications

Beyond the standard IS–LM–PC assumptions (closed economy, no capital mobility, etc.), this implementation makes the following modeling choices:

* **Expectations:** Inflation expectations are naive and adaptive:

$$
E_t[\pi_{t+1}] = \pi_t
$$

Expectations formed in period $t-1$ enter the Phillips curve for period $t$.

* **Phillips Curve:** Inflation evolves according to a standard expectations-augmented Phillips curve:

$$
\pi_t = E_{t-1}[\pi_t] + \alpha \cdot \text{output gap}_t
$$

* **Monetary Policy:** The central bank follows a Taylor rule for the nominal interest rate:

$$
i_t = r_n + \pi_t + \phi_{\pi}(\pi_t-\bar{\pi}) + \phi_{y}\left(\frac{Y_t-Y_n}{Y_n}\right)
$$

where $\phi_\pi, \phi_y > 0$ and $\bar{\pi}$ is the inflation target.

* **Output Determination:** Output each period is determined by a static IS relation with interest-sensitive investment and fiscal demand, solved conditional on the real interest rate.

The model evolves forward recursively period by period.

## Setup (Recommended)

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate      # macOS / Linux
# .venv\Scripts\activate       # Windows

pip install -r requirements.txt
```

## How To Run

This program is operated from the command line.

1. Navigate to the project root.
2. Run:

```bash
python main.py
```

This uses the defaults:

* Simulation length: 10 periods
* Parameters: `resources/parameters_baseline.csv`
* Shocks: `resources/shocks_baseline.csv`


### Modifying Defaults

Each default can be modified:

* **Number of periods (positional argument):**

```bash
python main.py 25
```

If provided, this must come first.

* **Alternative parameter file:**

```bash
python main.py -p alt_params.csv
```

Must be located in the `resources/` folder.

* **Alternative shock file:**

```bash
python main.py -s alt_shocks.csv
```

Must also be located in `resources/`.

### Examples

**Run baseline model for 25 periods**

```bash
python main.py 25
```

**Apply an alternative shock path using default parameters**

```bash
python main.py --shocks alt_shocks.csv
```

**Run a longer simulation with a custom shock schedule**

```bash
python main.py 50 -s inflation_shock.csv
```

**Change structural parameters while keeping baseline shocks**

```bash
python main.py 50 -p alt_params.csv
```

**Run a full counterfactual**

```bash
python main.py 100 --params alt_params.csv --shocks alt_shocks.csv
```

## Interpreting the Output

The model prints a `pandas` `DataFrame` containing key macroeconomic variables:

* **Y_n** — natural output
* **r_n** — natural real interest rate
* **pi_t** — inflation at time $t$
* **pi_e** — expected inflation for period $t+1$, formed at time $t$
* **pi_e_used** — expected inflation used in the Phillips curve for period $t$, i.e. $E_{t-1}[\pi_t]$
* **i_t** — nominal interest rate
* **Y_t** — output at time $t$

If plotting is enabled (with flag `--plot` or `-g`), the program displays the time paths of inflation and expected inflation used in the Phillips curve.

## Forthcoming Extensions

* Additional plotting and visualization tools
* Alternative expectation formation rules (e.g., partial adjustment or anchored expectations)
* Alternative monetary policy rules
* Richer persistence mechanisms in output and inflation dynamics
* Expanded financial or supply-side blocks
