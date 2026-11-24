import pathlib
from _typeshed import Incomplete
from typing import NamedTuple

ROOT: Incomplete
CATALOG: Incomplete
MODELS: Incomplete
LOG: Incomplete
TIMEOUT: int
COOLDOWNS_H: Incomplete
HOME: Incomplete
PLACES: Incomplete
MARKS: Incomplete
ANSWER_FLOOR: int

class Result(NamedTuple):
    worker: str
    model: str
    status: str
    text: str
    seconds: float

def table(path: pathlib.Path) -> list[dict]: ...
def catalog() -> list[dict]: ...
def cooling(worker: str, now: str = '') -> str: ...
def chain(now: str = '') -> list[dict]: ...
def find(harness: str) -> str | None: ...
def run(cmd: list[str], cwd: str | None = None, timeout: int = ...) -> tuple[int, str]: ...
def classify(code: int, text: str) -> str: ...

ADAPTERS: Incomplete

def call(worker: str, prompt: str, role: str = '-', cwd: str | None = None) -> Result: ...
def record(result: Result, role: str = '-') -> None: ...
def tally() -> dict: ...

OFFERS: Incomplete

def offered(harness: str) -> set | None: ...
def live(row: dict, offers: dict | None = None) -> str: ...
