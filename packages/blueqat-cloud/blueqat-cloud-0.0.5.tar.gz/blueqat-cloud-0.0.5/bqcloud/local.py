"""For local task."""

import typing
from typing import Optional

from blueqat import Circuit

from .abstract_result import AbstractResult
from .data import Status
from .task import AbstractTask

class LocalResult(AbstractResult):
    def __init__(self, shots: typing.Counter[str]):
        self._shots = shots

    def shots(self) -> typing.Counter[str]:
        return self._shots


class LocalTask(AbstractTask):
    """Task for local simulator."""
    def __init__(self, circuit: Circuit, result: LocalResult) -> None:
        self.circuit = circuit
        self.result = result

    def status(self) -> Status:
        return Status.COMPLETED

    def update(self) -> None:
        pass

    def __repr__(self) -> str:
        return f'LocalTask({self.circuit}, {self.result})'

    def wait(self, timeout: int = 0) -> Optional[AbstractResult]:
        return self.result

    def result(self):
        return self.result


def make_localtask(c: Circuit, shots: int):
    return LocalTask(c, LocalResult(c.copy().m[:].run(shots=shots)))
