import matplotlib.pyplot as plt
import pandas as pd
from dataclasses import dataclass, field


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


def make_figure(df: pd.DataFrame):
    fig, axs = plt.subplot_mosaic([["Y", "Y"], ["i", "pi"]])

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
            df=df[["pi_t", "pi_e"]],
            title="Inflation Rates",
            labels={
                "pi_t": r"Inflation Rate ($\pi_t$)",
                "pi_e": r"Expected Inflation Rate ($\pi_t^e$)",
            },
        ),
    }

    for key, info in specs.items():
        plot_info(axs[key], info)

    fig.tight_layout()
    return fig, axs


def display_plots(df: pd.DataFrame):
    fig, _ = make_figure(df=df)
    plt.show()
    return fig
