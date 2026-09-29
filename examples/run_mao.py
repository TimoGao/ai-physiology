import json
from mao.experiment import run_all_experiments

if __name__ == "__main__":
    result = run_all_experiments(seed=7)
    print(json.dumps(result, indent=2, ensure_ascii=False))
