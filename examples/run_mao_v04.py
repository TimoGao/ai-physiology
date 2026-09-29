from mao.experiment_v04 import export_results, run_matrix

if __name__ == "__main__":
    result = run_matrix(range(30))
    paths = export_results(result, "results/mao-v0.4")
    print("MAO Experiment v0.4 complete")
    for name, path in paths.items():
        print(f"{name}: {path}")
