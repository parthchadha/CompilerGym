# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""This module defines and registers the example gym environments."""
from pathlib import Path
from typing import Iterable

from compiler_gym.datasets import Benchmark, Dataset
from compiler_gym.datasets.uri import BenchmarkUri
from compiler_gym.spaces import Reward
from compiler_gym.util.registration import register
from compiler_gym.util.runfiles_path import runfiles_path

EXAMPLE_CC_SERVICE_BINARY: Path = runfiles_path(
    "examples/example_compiler_gym_service/service_cc/compiler_gym-example-service-cc"
)

EXAMPLE_PY_SERVICE_BINARY: Path = runfiles_path(
    "examples/example_compiler_gym_service/service_py/compiler_gym-example-service-py"
)


class RuntimeReward(Reward):
    """An example reward that uses changes in the "runtime" observation value
    to compute incremental reward.
    """

    def __init__(self):
        super().__init__(
            name="runtime",
            observation_spaces=["runtime"],
            default_value=0,
            default_negates_returns=True,
            deterministic=False,
            platform_dependent=True,
        )
        self.previous_runtime = None

    def reset(self, benchmark: str, observation_view):
        del benchmark  # unused
        self.previous_runtime = None

    def update(self, action, observations, observation_view):
        del action
        del observation_view

        if self.previous_runtime is None:
            self.previous_runtime = observations[0]

        reward = float(self.previous_runtime - observations[0])
        self.previous_runtime = observations[0]
        return reward


class ExampleDataset(Dataset):
    def __init__(self, *args, **kwargs):
        super().__init__(
            name="benchmark://example-v0",
            license="MIT",
            description="An example dataset",
        )
        self._benchmarks = {
            "/foo": Benchmark.from_file_contents(
                "benchmark://example-v0/foo", "Ir data".encode("utf-8")
            ),
            "/bar": Benchmark.from_file_contents(
                "benchmark://example-v0/bar", "Ir data".encode("utf-8")
            ),
        }

    def benchmark_uris(self) -> Iterable[str]:
        yield from (f"benchmark://example-v0{k}" for k in self._benchmarks.keys())

    def benchmark_from_parsed_uris(self, uri: BenchmarkUri) -> Benchmark:
        if uri.path in self._benchmarks:
            return self._benchmarks[uri]
        else:
            raise LookupError("Unknown program name")


# Register the example service on module import. After importing this module,
# the example-v0 environment will be available to gym.make(...).
register(
    id="example-cc-v0",
    entry_point="compiler_gym.envs:CompilerEnv",
    kwargs={
        "service": EXAMPLE_CC_SERVICE_BINARY,
        "rewards": [RuntimeReward()],
        "datasets": [ExampleDataset()],
    },
)

register(
    id="example-py-v0",
    entry_point="compiler_gym.envs:CompilerEnv",
    kwargs={
        "service": EXAMPLE_PY_SERVICE_BINARY,
        "rewards": [RuntimeReward()],
        "datasets": [ExampleDataset()],
    },
)
