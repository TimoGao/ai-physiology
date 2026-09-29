from mao.cross_system_v053 import export_results, run_benchmark

if __name__ == "__main__":
    result = run_benchmark(
        calibration_seeds=range(500),
        evaluation_seeds=range(500, 1000),
        cycles=240,
    )
    paths = export_results(result, "results/mao-v0.5.3")
    print("MAO v0.5.3 complete")
    for name, path in paths.items():
        print(f"{name}: {path}")
