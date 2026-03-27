from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class AppConfig:
    """
    Configuration for standalone quadratic scatter application.
    """

    # Excel file containing experiment root paths
    # Example path stored in Excel:
    # C:\Users\mt1102\Box\Nabeel Tahir Meetings\Meetings\Weekly Meetings\Meeting March 2026\Experiment 3_18_2026
    excel_file: str = r"C:\Users\mt1102\Documents\Python Scripts\CellTrackScatterPlots\LinktoExperiments.xlsx"

    # Column in Excel that stores experiment root path
    experiment_path_column: str = "experiment_path"

    # Optional label column in Excel
    experiment_label_column: str = "experiment_label"

    # Samples to process
    sample_names: List[str] = field(default_factory=lambda: ["Sample 1", "Sample 2"])

    # Sample -> run mapping
    sample_run_map: Dict[str, str] = field(default_factory=lambda: {
        "Sample 1": "S1 V1 2uL",
        "Sample 2": "S2 V1 2uL",
    })

    # Conditions to process
    conditions: List[str] = field(default_factory=lambda: ["Stained", "Unstained"])

    # Folder names
    quad_folder_name: str = "Quad"
    linear_folder_name: str = "Linear"

    # File names
    a2_filename: str = "deflection_summary_a2_quad_gate.csv"
    b1_filename: str = "deflection_summary_b1_quad_gate.csv"
    slope_filename: str = "deflection_summary_slope_inverted_gate.csv"

    # Output filenames inside Quad folder
    merged_output_filename: str = "quad_scatter_data.csv"
    scatter_output_filename: str = "a2_vs_b1_scatter.png"

    # Plot settings
    figure_dpi: int = 300
    annotate_ids: bool = False
    use_linear_classification_for_color: bool = True
    show_plot: bool = False