import itertools
import statistics
import time
from typing import Callable, Iterator

import pandas as pd
from onnxruntime import ExecutionMode, ExecutionOrder, SessionOptions

DEFAULT_SESSION_OPTIONS = {
    "enable_cpu_mem_arena": True,
    "enable_mem_pattern": True,
    "execution_mode": ExecutionMode.ORT_SEQUENTIAL,
    "execution_order": ExecutionOrder.DEFAULT,
    "inter_op_num_threads": 0,
    "intra_op_num_threads": 0,
    "use_deterministic_compute": False,
}

SESSION_OPTIONS = {
    "enable_cpu_mem_arena": [True, False],
    "enable_mem_pattern": [True, False],
    "execution_mode": [ExecutionMode.ORT_SEQUENTIAL, ExecutionMode.ORT_PARALLEL],
    "execution_order": [ExecutionOrder.DEFAULT, ExecutionOrder.PRIORITY_BASED],
    "inter_op_num_threads": [0, 1, 2],
    "intra_op_num_threads": [0, 1, 2],
    "use_deterministic_compute": [True, False],
}


class ONNXSearchSpace:
    @property
    def configs(self) -> list[SessionOptions]:
        k, values = zip(*SESSION_OPTIONS.items())
        return [DEFAULT_SESSION_OPTIONS] + [dict(zip(k, v)) for v in itertools.product(*values)]

    def __iter__(self) -> Iterator[SessionOptions]:
        keys, values = zip(*SESSION_OPTIONS.items())
        configs = [dict(zip(keys, v)) for v in itertools.product(*values)]
        for config in self.configs:
            options = SessionOptions()
            for key, value in config.items():
                setattr(options, key, value)
            yield options

    def __len__(self) -> int:
        return len(self.configs)


class Timer:
    def __init__(self, num_loops: int = 1_000):
        self.num_loops = num_loops
        self._history = {}

    @property
    def history(self):
        return {
            task: {
                "mean": statistics.mean(times),
                "median": statistics.median(times),
                "stdev": statistics.stdev(times),
            }
            for task, times in self._history.items()
        }

    def summary(self):
        return pd.DataFrame(self.history).T.sort_values("median")

    def plot(self):
        ax = pd.DataFrame(self._history).plot.box(vert=False)
        ax.set_xlabel("time (ms)")
        ax.set_xlim(0)

    def evaluate(self, f: Callable, x: str, verbosity: int = 1, return_median: bool = False):
        self._history[f.__name__] = []

        for _ in range(self.num_loops):
            start_time = time.time()
            f(x)
            end_time = time.time()
            self._history[f.__name__].append((end_time - start_time) * 1000)

        if verbosity > 0:
            print(f"{f.__name__}: {self.history[f.__name__]}")
        if return_median:
            return statistics.median(self._history[f.__name__])

    @property
    def best_time(self) -> float:
        return min(self.history.values(), key=self._select_median)

    @property
    def baseline(self) -> float:
        return self.history["simple_pipeline"]

    @staticmethod
    def _select_median(values: dict[str, float]) -> float:
        return values["median"]
