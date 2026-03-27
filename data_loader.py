from pathlib import Path
from typing import Optional

import pandas as pd


def read_csv_if_exists(csv_path: Path) -> Optional[pd.DataFrame]:
    """
    Read CSV if it exists, otherwise return None.
    """
    if not csv_path.exists():
        print(f"[WARN] File not found: {csv_path}")
        return None

    try:
        return pd.read_csv(csv_path)
    except Exception as exc:
        print(f"[ERROR] Failed to read CSV: {csv_path}\nReason: {exc}")
        return None


def load_experiment_table(excel_file: str, experiment_path_column: str) -> pd.DataFrame:
    """
    Load Excel file containing experiment paths.
    """
    df = pd.read_excel(excel_file)

    if experiment_path_column not in df.columns:
        raise ValueError(
            f"Column '{experiment_path_column}' not found in Excel file.\n"
            f"Available columns: {list(df.columns)}"
        )

    df = df[df[experiment_path_column].notna()].copy()
    return df


def _standardize_bool_column(df: pd.DataFrame, col_name: str) -> pd.DataFrame:
    """
    Convert a mixed boolean-like column to True / False / NaN.
    """
    if col_name not in df.columns:
        return df

    mapping = {
        "true": True,
        "false": False,
        "1": True,
        "0": False,
        "yes": True,
        "no": False,
    }

    def convert_value(val):
        if pd.isna(val):
            return pd.NA
        if isinstance(val, bool):
            return val
        sval = str(val).strip().lower()
        return mapping.get(sval, pd.NA)

    df[col_name] = df[col_name].apply(convert_value)
    return df


def load_quadratic_and_linear_data(
    quad_dir: Path,
    linear_dir: Path,
    a2_filename: str,
    b1_filename: str,
    slope_filename: str,
) -> Optional[pd.DataFrame]:
    """
    Load:
      - deflection_summary_a2_quad_gate.csv
      - deflection_summary_b1_quad_gate.csv
      - optionally deflection_summary_slope_inverted_gate.csv

    Merge all by particle id.
    """
    a2_path = quad_dir / a2_filename
    b1_path = quad_dir / b1_filename
    slope_path = linear_dir / slope_filename

    df_a2 = read_csv_if_exists(a2_path)
    df_b1 = read_csv_if_exists(b1_path)

    if df_a2 is None or df_b1 is None:
        return None

    required_a2 = {"id", "a2_quad"}
    required_b1 = {"id", "b1_quad"}

    if not required_a2.issubset(df_a2.columns):
        print(f"[ERROR] Missing required columns in {a2_path}. Required: {required_a2}")
        return None

    if not required_b1.issubset(df_b1.columns):
        print(f"[ERROR] Missing required columns in {b1_path}. Required: {required_b1}")
        return None

    df_a2_small = df_a2[["id", "a2_quad"]].copy()
    df_b1_small = df_b1[["id", "b1_quad"]].copy()

    merged = pd.merge(df_a2_small, df_b1_small, on="id", how="inner")

    df_slope = read_csv_if_exists(slope_path)
    if df_slope is not None and "id" in df_slope.columns:
        candidate_cols = ["id", "slope_inverted", "slope_raw", "is_deflected"]
        available_cols = [c for c in candidate_cols if c in df_slope.columns]
        df_slope_small = df_slope[available_cols].copy()
        df_slope_small = _standardize_bool_column(df_slope_small, "is_deflected")
        merged = pd.merge(merged, df_slope_small, on="id", how="left")

    numeric_cols = ["a2_quad", "b1_quad", "slope_inverted", "slope_raw"]
    for col in numeric_cols:
        if col in merged.columns:
            merged[col] = pd.to_numeric(merged[col], errors="coerce")

    merged = merged.dropna(subset=["id", "a2_quad", "b1_quad"]).copy()

    return merged