from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def save_merged_dataframe(df: pd.DataFrame, output_csv: Path) -> None:
    """
    Save merged dataframe to CSV.
    """
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_csv, index=False)


def create_quadratic_scatter_plot(
    df: pd.DataFrame,
    output_png: Path,
    title: str,
    annotate_ids: bool = False,
    use_linear_classification_for_color: bool = True,
    dpi: int = 300,
    show_plot: bool = False,
) -> None:
    """
    Create scatter plot of a2_quad vs b1_quad.
    Saves directly to the specified PNG path.
    """

    plt.figure(figsize=(8, 6))

    if use_linear_classification_for_color and "is_deflected" in df.columns:
        df_not_deflected = df[df["is_deflected"] == False]
        df_deflected = df[df["is_deflected"] == True]
        df_unknown = df[df["is_deflected"].isna()]

        if not df_not_deflected.empty:
            plt.scatter(
                df_not_deflected["a2_quad"],
                df_not_deflected["b1_quad"],
                marker="o",
                alpha=0.8,
                label="Not deflected",
            )

        if not df_deflected.empty:
            plt.scatter(
                df_deflected["a2_quad"],
                df_deflected["b1_quad"],
                marker="x",
                alpha=0.8,
                label="Deflected",
            )

        if not df_unknown.empty:
            plt.scatter(
                df_unknown["a2_quad"],
                df_unknown["b1_quad"],
                marker="s",
                alpha=0.8,
                label="Unknown",
            )
    else:
        plt.scatter(
            df["a2_quad"],
            df["b1_quad"],
            marker="o",
            alpha=0.8,
            label="Cells",
        )

    if annotate_ids and "id" in df.columns:
        for _, row in df.iterrows():
            plt.annotate(
                str(row["id"]),
                (row["a2_quad"], row["b1_quad"]),
                fontsize=7,
                alpha=0.7,
            )

    plt.xlabel("a2_quad")
    plt.ylabel("b1_quad")
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    output_png.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_png, dpi=dpi, bbox_inches="tight")

    if show_plot:
        plt.show()

    plt.close()