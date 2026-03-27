from pathlib import Path

from config import AppConfig
from data_loader import load_experiment_table, load_quadratic_and_linear_data
from path_utils import build_sample_paths, get_existing_samples
from plotter import create_quadratic_scatter_plot, save_merged_dataframe


def get_experiment_label(row, cfg: AppConfig, experiment_root: str) -> str:
    """
    Get experiment label from Excel if available; otherwise use folder name.
    """
    if cfg.experiment_label_column in row.index:
        raw_label = str(row[cfg.experiment_label_column]).strip()
        if raw_label and raw_label.lower() != "nan":
            return raw_label

    return Path(experiment_root).name


def get_condition_paths(all_paths: dict, condition: str):
    """
    Return quad_dir and linear_dir based on condition.
    """
    if condition == "Stained":
        return all_paths["stained_quad"], all_paths["stained_linear"]
    elif condition == "Unstained":
        return all_paths["unstained_quad"], all_paths["unstained_linear"]
    else:
        raise ValueError(f"Unsupported condition: {condition}")


def process_one_condition(
    experiment_root: str,
    experiment_label: str,
    sample_name: str,
    run_name: str,
    condition: str,
    cfg: AppConfig,
) -> None:
    """
    Process one experiment/sample/condition combination.
    Save outputs directly into the Quad folder.
    """
    all_paths = build_sample_paths(experiment_root, sample_name, run_name)
    quad_dir, linear_dir = get_condition_paths(all_paths, condition)

    print("=" * 100)
    print(f"[INFO] Experiment : {experiment_label}")
    print(f"[INFO] Sample     : {sample_name}")
    print(f"[INFO] Condition  : {condition}")
    print(f"[INFO] Run        : {run_name}")
    print(f"[INFO] Quad dir   : {quad_dir}")
    print(f"[INFO] Linear dir : {linear_dir}")

    if not quad_dir.exists():
        print(f"[WARN] Quad directory does not exist: {quad_dir}")
        return

    df = load_quadratic_and_linear_data(
        quad_dir=quad_dir,
        linear_dir=linear_dir,
        a2_filename=cfg.a2_filename,
        b1_filename=cfg.b1_filename,
        slope_filename=cfg.slope_filename,
    )

    if df is None or df.empty:
        print("[WARN] No usable data found for this combination.")
        return

    merged_csv_path = quad_dir / cfg.merged_output_filename
    scatter_png_path = quad_dir / cfg.scatter_output_filename

    save_merged_dataframe(df, merged_csv_path)

    plot_title = (
        f"{experiment_label} | {sample_name} | {condition} | {run_name}\n"
        f"a2_quad vs b1_quad"
    )

    create_quadratic_scatter_plot(
        df=df,
        output_png=scatter_png_path,
        title=plot_title,
        annotate_ids=cfg.annotate_ids,
        use_linear_classification_for_color=cfg.use_linear_classification_for_color,
        dpi=cfg.figure_dpi,
        show_plot=cfg.show_plot,
    )

    print(f"[DONE] Saved merged data  : {merged_csv_path}")
    print(f"[DONE] Saved scatter plot : {scatter_png_path}")


def main() -> None:
    cfg = AppConfig()

    experiment_df = load_experiment_table(
        excel_file=cfg.excel_file,
        experiment_path_column=cfg.experiment_path_column,
    )

    for _, row in experiment_df.iterrows():
        experiment_root = str(row[cfg.experiment_path_column]).strip()
        experiment_label = get_experiment_label(row, cfg, experiment_root)

        existing_samples = get_existing_samples(
            experiment_root=experiment_root,
            candidate_samples=cfg.sample_names,
        )

        if not existing_samples:
            print("=" * 100)
            print(f"[WARN] No sample folders found in experiment: {experiment_root}")
            continue

        print("=" * 100)
        print(f"[INFO] Found samples for {experiment_label}: {existing_samples}")

        for sample_name in existing_samples:
            if sample_name not in cfg.sample_run_map:
                print(f"[WARN] No run mapping found for {sample_name}. Skipping.")
                continue

            run_name = cfg.sample_run_map[sample_name]

            for condition in cfg.conditions:
                process_one_condition(
                    experiment_root=experiment_root,
                    experiment_label=experiment_label,
                    sample_name=sample_name,
                    run_name=run_name,
                    condition=condition,
                    cfg=cfg,
                )


if __name__ == "__main__":
    main()