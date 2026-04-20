import asyncio
import time
from typing import Awaitable, Callable

from .signal import Signal


class SignalMonitor:
    def __init__(self, signals: list[Signal],
                 ui_func: Callable[[list[str]], Awaitable[None]],
                 interval: float = 0.3
                 ) -> None:
        self.signals = signals
        self.interval = interval
        self.ui_func = ui_func
        self.task: asyncio.Task | None = None

    def start(self) -> None:
        if self.task is not None and not self.task.done():
            return
        self.task = asyncio.create_task(self.run())

    async def stop(self) -> None:
        if self.task is None:
            return
        self.task.cancel()
        try:
            await self.task
        except asyncio.CancelledError:
            pass
        finally:
            self.task = None

    async def run(self) -> None:
        try:
            while True:
                lines = ["PLC STATES", ""]
                start = time.perf_counter()
                for signal in self.signals:
                    try:
                        await signal.get_state()
                        lines.append(f"{signal.name:<18}: {signal.state}")
                    except Exception as exc:
                        lines.append(f"{signal.name:<18}: ERROR ({exc})")

                lines.extend([
                    "Controls",
                    "s = start conveyor",
                    "x = stop conveyor",
                    "q = quit",
                ])

                await self.ui_func(lines)
                elapsed = time.perf_counter() - start
                wait_time = self.interval - elapsed
                await asyncio.sleep(max(0, wait_time))
        except asyncio.CancelledError:
            raise
