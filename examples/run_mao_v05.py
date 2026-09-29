from mao.experiment_v05 import export_results, run_matrix

if __name__ == "__main__":
    result = run_matrix(range(30))
    paths = export_results(result, "results/mao-v0.5")
    print("MAO v0.5 reliability integration complete")
    for name, path in paths.items():
        print(f"{name}: {path}")
