from pprint import pprint
from mao.experiment import run_chronic_degradation_experiment

if __name__ == "__main__":
    result = run_chronic_degradation_experiment(cycles=200, seed=7)
    pprint(result)
