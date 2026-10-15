"""Local guard for the provider's request quota, so we fall back before Google says 429.

Counts requests per minute and per rolling 24 hours, in this process only. With several
server workers, divide the limits by the number of workers.
"""

import threading
import time
from collections import deque
from collections.abc import Callable
from functools import cache


class QuotaGuard:
    def __init__(
        self,
        rpm: int,
        rpd: int = 0,
        cooldown_s: float = 60.0,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self.rpm = rpm
        self.rpd = rpd
        self.cooldown_s = cooldown_s
        self._clock = clock
        self._lock = threading.Lock()
        self._minute: deque[float] = deque()
        self._day: deque[float] = deque()
        self._blocked_until = 0.0

    def _prune(self, now: float) -> None:
        while self._minute and now - self._minute[0] >= 60:
            self._minute.popleft()
        while self._day and now - self._day[0] >= 86_400:
            self._day.popleft()

    def try_acquire(self, n: int = 1) -> bool:
        """Reserve `n` requests now, all or nothing. False = over the limit or cooling down."""
        with self._lock:
            now = self._clock()
            if now < self._blocked_until:
                return False
            self._prune(now)
            if self.rpm and len(self._minute) + n > self.rpm:
                return False
            if self.rpd and len(self._day) + n > self.rpd:
                return False
            for _ in range(n):
                self._minute.append(now)
                self._day.append(now)
            return True

    def note_rate_limited(self) -> None:
        """The provider answered 429: stop calling it for a while."""
        with self._lock:
            self._blocked_until = self._clock() + self.cooldown_s

    def snapshot(self) -> dict[str, float | int]:
        with self._lock:
            now = self._clock()
            self._prune(now)
            return {
                "used_last_minute": len(self._minute),
                "used_last_24h": len(self._day),
                "cooldown_left_s": round(max(0.0, self._blocked_until - now), 1),
            }


@cache
def shared_quota(rpm: int, rpd: int, cooldown_s: float) -> QuotaGuard:
    """One guard per process for every model call (scores and drugs share the quota)."""
    return QuotaGuard(rpm, rpd, cooldown_s)
