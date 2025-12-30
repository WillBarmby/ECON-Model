import matplotlib.pyplot as plt
from main import main
import pandas as pd

if __name__ == "__main__":

    fig, axs = plt.subplot_mosaic([["Y", "Y"], ["i", "pi"]])
    df: pd.DataFrame = main()
    Y_data: pd.DataFrame = df[["Y_n", "Y_t"]]
    i_data: pd.DataFrame = df[["i_t", "r_n"]]
    pi_data: pd.DataFrame = df[["pi_t", "pi_e"]]

    axs["Y"].set_title("Output")
    axs["Y"].plot(Y_data.index, Y_data["Y_n"], label="Natural Output ($Y_n$)")
    axs["Y"].plot(Y_data.index, Y_data["Y_t"], label="Actual Output ($Y_t$)")

    axs["i"].set_title("Interest Rates")
    axs["i"].plot(i_data.index, i_data["i_t"], label="Nominal Interest Rate ($i_t$)")
    axs["i"].plot(
        i_data.index, i_data["r_n"], label="Real Natural Interest Rate ($r_n$)"
    )

    axs["pi"].set_title("Inflation Rates")
    axs["pi"].plot(pi_data.index, pi_data["pi_t"], label=r"Inflation Rate ($\pi_t$)")
    axs["pi"].plot(
        pi_data.index, pi_data["pi_e"], label=r"Expected Inflation Rate ($\pi_t$)"
    )

    for ax in axs.values():
        ax.legend()

    fig.tight_layout()
    print(df.keys())
    print(axs.keys())
    plt.show()
