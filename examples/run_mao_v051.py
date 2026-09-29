from mao.longitudinal_v051 import run_benchmark
import json

if __name__ == "__main__":
    result = run_benchmark(range(200), cycles=240)
    print(json.dumps(result["summary"], ensure_ascii=False, indent=2))
