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
                start_time = time.perf_counter()

                io_signals = [s for s in self.signals if s.type == "io"]
                state_signals = [s for s in self.signals if s.type == "state"]

                io_rows: list[str] = []
                state_rows: list[str] = []
                IO_NAME = 20
                IO_STATE = 8

                STATE_NAME = 30
                STATE_STATE = 8

                for signal in io_signals:
                    try:
                        await signal.get_state()
                        io_rows.append(
                            f"{signal.name:<{IO_NAME}} {str(signal.state):<{IO_STATE}}")
                    except Exception as exc:
                        io_rows.append(
                            f"{signal.name:<{IO_NAME}}: ERROR ({exc})")

                for signal in state_signals:
                    try:
                        await signal.get_state()
                        state_rows.append(
                            f"{signal.name:<{STATE_NAME}} {str(signal.state):<{STATE_STATE}}")
                    except Exception as exc:
                        state_rows.append(
                            f"{signal.name:<{STATE_NAME}}: ERROR ({exc})")

                left_header = "INPUTS"
                right_header = "STATES"

                left_width = 30
                right_width = 50
                separator = "   |   "

                max_rows = max(len(io_rows), len(state_rows))

                while len(io_rows) < max_rows:
                    io_rows.append("")

                while len(state_rows) < max_rows:
                    state_rows.append("")

                lines = [
                    f"{left_header:<{left_width}}{separator}{right_header:<{right_width}}",
                    f"{'-' * left_width}{separator}{'-' * right_width}",
                ]

                for left, right in zip(io_rows, state_rows):
                    lines.append(
                        f"{left:<{left_width}}{separator}{right:<{right_width}}")

                await self.ui_func(lines)

                elapsed = time.perf_counter() - start_time
                wait_time = self.interval - elapsed
                await asyncio.sleep(max(0, wait_time))

        except asyncio.CancelledError:
            raise
