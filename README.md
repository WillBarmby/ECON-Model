# IS-LM-PC Simulator  

## What This Is

This is a simple, discrete-time simulator of the IS-LM-PC model of a closed macroeconomy. The program takes in a set of initial parameters and a shock schedule for those parameters, and returns the time path of a set of economic variables over a given number of periods. 
## Model Specifications

Beyond the standard IS-LM-PC assumptions (e.g. closed economy), this implementation makes the following modeling choices:
- $\pi_{t+1}^{e} \equiv \pi_{t}$, i.e. inflation expectations are adaptive and one-period ahead.
- The central bank of this economy follows a Taylor rule for setting the nominal interest rate: 
$$i_t = r_n + \pi_t + \phi_{\pi}(\pi_t-\bar{\pi}) + \phi_{y}\left(\frac{Y_t-Y_n}{Y_n}\right)$$
where $\phi_\pi, \phi_y > 0$ and $\bar{\pi}$ is the inflation target.

- Expectations update contemporaneously (no information lag).

## How To Run
This program is operated from the command line. 
1. Navigate to project root
2. Type and enter `python main.py`
	1. This runs with the defaults: 
		1. The simulation runs for 10 periods ($T= 10$)
		2. The parameters are stored in `params_baseline.csv`
		3. The shocks are stored in `shocks_baseline.csv`
3. Each of these defaults can be modified with the following tags:
	1. `t`: A positional argument for the number of periods ($T$)
		1. e.g. `python main.py 25`
		2. if entered, this must be the first tag
	2. `--params` or `-p` for the .csv file storing the initial parameters. Must be located in the project's `resources` folder, with the same parameters and headings as stored in `params_baseline.csv`
	3. `--shocks`  or `-s` for the .csv storing the shocks to the parameters.  Must be stored in the project's `resources` folder, with the same parameters and headings as stored in `shocks_baseline.csv`

### Examples

**Run the baseline model for 25 periods**
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

**Run a full counterfactual with custom parameters and shocks**

```bash
python main.py 100 --params alt_params.csv --shocks alt_shocks.csv
```

**Run a short diagnostic simulation with custom inputs**

```bash
python main.py 10 -p alt_params.csv -s alt_shocks.csv
```


## Interpreting the Output

At present, the model prints the rows of a `pandas` `DataFrame` after it runs, containing several key macroeconomic variables: 
- $Y_n$: the natural output of this economy
- $r_n$: the natural real interest rate for this economy
- $pi_t$: inflation at time $t$
- $pi_e$: expected inflation for period $t+1$, formed at time $t$. 
- $i_t$: the nominal rate at time $t$
- $Y_t$: the level of output at time $t$

## Forthcoming Extensions
- Plots and animations for simulation results
- CLI tags for pluggable/replaceable assumptions, such as:
	- lagged vs. up to date expectations
	- different central bank policy
	- different ways for inflation expectations to be set over time
