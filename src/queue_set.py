# Standard Library
from collections import deque
from typing import Any


class queue(deque):
    @property
    def seen(self):
        if not hasattr(self, "_seen"):
            self._seen = set()
        return self._seen

    def append(self, __x: Any) -> None:
        if __x in self.seen:
            return

        self.seen.add(__x)
        return super().append(__x)
