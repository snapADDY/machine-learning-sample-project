import itertools
import statistics
import time
from collections.abc import Callable, Iterator

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
    """Search space over ONNX session options."""

    @property
    def configs(self) -> list[SessionOptions]:
        """Create a list of configurations."""
        # extract the keys and the list of values for each key
        keys = list(SESSION_OPTIONS)
        values = [SESSION_OPTIONS[key] for key in keys]

        # Build the list of dictionaries for each combination
        return [DEFAULT_SESSION_OPTIONS] + [
            {key: value for key, value in zip(keys, combination, strict=False)}
            for combination in itertools.product(*values)
        ]

    def __iter__(self) -> Iterator[SessionOptions]:
        """Iterate over the configurations."""
        for config in self.configs:
            options = SessionOptions()
            for key, value in config.items():
                setattr(options, key, value)
            yield options

    def __len__(self) -> int:
        """Get the number of configurations."""
        return len(self.configs)


class Timer:
    """Timer to profile runtime and stuff."""

    def __init__(self, num_loops: int = 1_000):
        self.num_loops = num_loops
        self._history = {}

    @property
    def history(self):
        """Return the history of the timer."""
        return {
            task: {
                "mean": statistics.mean(times),
                "median": statistics.median(times),
                "stdev": statistics.stdev(times),
            }
            for task, times in self._history.items()
        }

    def summary(self):
        """Get a summary."""
        return pd.DataFrame(self.history).T.sort_values("median")

    def plot(self):
        """Plot the history."""
        df = pd.DataFrame(self._history)
        medians = df.median().sort_values(ascending=False)
        ax = df[medians.index].plot.box(vert=False)
        ax.set_xlabel("time (ms)")
        ax.set_xlim(0)

    def evaluate(
        self,
        f: Callable,
        x: str,
        *,
        verbosity: int = 1,
        return_median: bool = False,
    ) -> float | None:
        """Evaluate the function `f` with input `x`.

        Parameters
        ----------
        f : Callable
            Function to evaluate.
        x : str
            Input to the function.
        verbosity : int, optional
            Verbosity level, by default 1.
        return_median : bool, optional
            If True, return the median time, by default False.

        Returns
        -------
        float | None
            Median time if `return_median` is True, None otherwise.
        """
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

        return None

    @property
    def best_time(self) -> float:
        """Best time."""
        return min(self.history.values(), key=self._select_median)

    @property
    def baseline(self) -> float:
        """Baseline time."""
        return self.history["simple_pipeline"]

    @staticmethod
    def _select_median(values: dict[str, float]) -> float:
        """Select the median value from a dictionary."""
        return values["median"]
