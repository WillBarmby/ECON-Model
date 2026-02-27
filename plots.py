import matplotlib.pyplot as plt
import pandas as pd
from dataclasses import dataclass, field

import matplotlib.ticker as mticker


@dataclass
class PlotInfo:
    df: pd.DataFrame
    title: str
    labels: dict[str, str] = field(default_factory=dict)

    def __post_init__(self):
        for key in self.labels:
            if key not in self.df.columns:
                raise ValueError(f"{key} not in dataframe columns")


def plot_info(ax, info: PlotInfo):
    ax.set_title(info.title)
    for col, label in info.labels.items():
        ax.plot(info.df.index, info.df[col], label=label)
    ax.legend()


def _configure_time_axis(axs: dict, df: pd.DataFrame, max_xticks: int = 25):
    """
    Make x-axis show every integer period for short runs,
    but automatically thin labels for long runs.
    """
    # robustly infer index span even if index isn’t RangeIndex
    x_min = int(df.index.min())
    x_max = int(df.index.max())
    n_periods = x_max - x_min + 1

    for ax in axs.values():
        ax.set_xlim(x_min, x_max)

        # Integer ticks only
        ax.xaxis.set_major_locator(
            mticker.MaxNLocator(nbins=max_xticks, integer=True, min_n_ticks=2)
        )

        # If it's short, force every period tick
        if n_periods <= max_xticks:
            ax.xaxis.set_major_locator(mticker.MultipleLocator(1))


def _configure_inflation_axis(ax):
    """
    Only the inflation subplot gets percent formatting.
    Assumes pi is stored as a decimal (e.g., 0.025 for 2.5%).
    """
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1.0))


def make_figure(df: pd.DataFrame):
    fig, axs = plt.subplot_mosaic(
        [["Y", "Y"], ["i", "pi"]], constrained_layout=True, figsize=(12, 7)
    )
    specs = {
        "Y": PlotInfo(
            df=df[["Y_n", "Y_t"]],
            title="Output",
            labels={
                "Y_n": r"Natural Output ($Y_n$)",
                "Y_t": r"Actual Output ($Y_t$)",
            },
        ),
        "i": PlotInfo(
            df=df[["i_t", "r_n"]],
            title="Interest Rates",
            labels={
                "i_t": r"Nominal Interest Rate ($i_t$)",
                "r_n": r"Real Natural Interest Rate ($r_n$)",
            },
        ),
        "pi": PlotInfo(
            df=df[["pi_t", "pi_e_used"]],
            title="Inflation Rates",
            labels={
                "pi_t": r"Inflation Rate ($\pi_t$)",
                "pi_e_used": r"Expected Inflation Rate for Period ($E_{t-1}[\pi_t]$)",
            },
        ),
    }

    for key, info in specs.items():
        plot_info(axs[key], info)

    # x-axis ticks: show all for small T, thin for big T
    _configure_time_axis(axs, df, max_xticks=25)

    # percent y-axis only for inflation
    _configure_inflation_axis(axs["pi"])

    return fig, axs


def display_plots(df: pd.DataFrame):
    fig, _ = make_figure(df=df)
    plt.show()
    return fig
