import asyncio
import random

from .signal import Signal


class DispatchController:
    def __init__(self, part_signal: Signal, dispatch_time: float = 0.5, auto_dispatch: bool = True) -> None:
        self.part_signal = part_signal
        self.dispatch_time = dispatch_time
        self.auto_dispatch = auto_dispatch
        self.task: asyncio.Task | None = None

    def start(self) -> None:
        if self.task is not None and not self.task.done():
            return
        self.task = asyncio.create_task(self._run())

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

    async def _run(self) -> None:
        try:
            while True:
                self.part_signal.pulse()
                if self.auto_dispatch:
                    await asyncio.sleep(random.uniform(0.0, 1.0))
                else:
                    await asyncio.sleep(self.dispatch_time)
        except asyncio.CancelledError:
            raise
