from enum import Enum


class Mark(Enum):
    """Mark/command from user"""
    clear = -1
    xz = 0
    one = 1
    two = 2
    three = 3
    five = 5
    eight = 8
    decompose = 9

    def is_mark(self) -> bool:
        return Mark.xz.value < self.value < Mark.decompose.value

    def get_mark(self) -> str:
        return str(self.value) if self.is_mark() else str(self.name)


class State(Enum):
    """User state"""
    thinking = 0
    ready = 1


class User:
    """User"""

    __slots__ = ("name", "_mark", "ws")

    def __init__(self, name: str, ws):
        self.name: str = name
        self._mark: Mark = Mark.clear
        self.ws = ws

    @property
    def state(self):
        return State.ready if self.mark is not Mark.clear else State.thinking

    def vote(self, mark: str):
        try:
            self._mark = Mark(int(mark))
        except ValueError:
            self._mark = None
            raise RuntimeError(f"User {self.name} send bad mark {mark}")

    def reset_mark(self):
        self._mark = Mark.clear

    @property
    def mark(self):
        return self._mark

    def as_dict(self):
        return dict(name=self.name, state=self.state.value, mark=self._mark.get_mark())
