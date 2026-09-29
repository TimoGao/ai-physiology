from pathlib import Path
import json

from mao.evaluation import (
    build_comparison_table,
    export_csv,
    export_json,
    run_experiment_matrix,
)

if __name__ == "__main__":
    output_dir = Path("results/mao-v0.3")
    result = run_experiment_matrix(
        seeds=range(10),
        baseline_kinds=("naive", "strong"),
    )

    json_path = export_json(result, output_dir / "results.json")
    csv_path = export_csv(result, output_dir / "runs.csv")

    print("MAO Experiment v0.3 complete")
    print(f"JSON: {json_path}")
    print(f"CSV:  {csv_path}")
    print(json.dumps(build_comparison_table(result), ensure_ascii=False, indent=2))
