
from datetime import datetime, timezone
from time import time


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def timestamp_ms() -> int:
    return int(time() * 1000)
