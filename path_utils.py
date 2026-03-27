from pathlib import Path
from typing import Dict, List


def build_sample_paths(experiment_root: str, sample_name: str, run_name: str) -> Dict[str, Path]:
    """
    Build all relevant paths for one sample in one experiment.
    """
    root = Path(experiment_root)

    stained_run_dir = root / sample_name / "Stained" / run_name
    unstained_run_dir = root / sample_name / "Unstained" / run_name

    return {
        "sample_dir": root / sample_name,
        "stained_run": stained_run_dir,
        "unstained_run": unstained_run_dir,
        "stained_quad": stained_run_dir / "Quad",
        "unstained_quad": unstained_run_dir / "Quad",
        "stained_linear": stained_run_dir / "Linear",
        "unstained_linear": unstained_run_dir / "Linear",
    }


def get_existing_samples(experiment_root: str, candidate_samples: List[str]) -> List[str]:
    """
    Return only the sample folders that actually exist in this experiment.
    Example:
      if only 'Sample 1' exists, return ['Sample 1']
    """
    root = Path(experiment_root)
    existing = []

    for sample_name in candidate_samples:
        if (root / sample_name).exists():
            existing.append(sample_name)

    return existing