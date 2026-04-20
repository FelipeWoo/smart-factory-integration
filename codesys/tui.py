import asyncio
import random

from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Static

from .helpers import pulse
from .signal import Signal


class PlcTui(App):
    CSS = """
    Screen {
        layout: vertical;
    }

    #states {
        height: 1fr;
        padding: 1 2;
        border: solid green;
    }
    """

    BINDINGS = [
        ("s", "start", "Start"),
        ("x", "stop", "Stop"),
        ("q,escape", "quit", "Quit"),
    ]

    def __init__(self, signals: list[Signal]) -> None:
        super().__init__()
        self.signals = signals
        self.signal_map = {signal.name: signal for signal in signals}
        self.monitor_task: asyncio.Task | None = None
        self.part_cycle_task: asyncio.Task | None = None

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Connecting...", id="states")
        yield Footer()

    async def on_mount(self) -> None:
        self.monitor_task = asyncio.create_task(self.monitor_loop())

    async def monitor_loop(self) -> None:
        try:
            while True:
                await self.refresh_states()
                await asyncio.sleep(0.3)
        except asyncio.CancelledError:
            raise

    async def refresh_states(self) -> None:
        lines = ["PLC STATES", ""]

        for signal in self.signals:
            try:
                await signal.get_state()
                lines.append(f"{signal.name:<18}: {signal.state}")
            except Exception as exc:
                lines.append(f"{signal.name:<18}: ERROR ({exc})")

        part_cycle_running = (
            self.part_cycle_task is not None and not self.part_cycle_task.done()
        )

        lines.extend([
            "",
            f"part_cycle_running : {part_cycle_running}",
            "",
            "Controls",
            "s = start conveyor + start part cycle",
            "x = stop conveyor + stop part cycle",
            "q = quit",
        ])

        self.query_one("#states", Static).update("\n".join(lines))

    async def safe_pulse(self, signal_name: str) -> None:
        signal = self.signal_map.get(signal_name)

        if signal is None:
            return

        try:
            await pulse(signal)
        except Exception as exc:
            self.query_one("#states", Static).update(
                f"Write error on {signal_name}:\n{exc}"
            )

    async def part_cycle_loop(self) -> None:
        signal = self.signal_map.get("bPartDetected")
        if signal is None:
            return

        try:
            while True:
                await pulse(signal)
                await asyncio.sleep(random.uniform(0.0, 1.0))
        except asyncio.CancelledError:
            raise

    async def start_part_cycle(self) -> None:
        if self.part_cycle_task is not None and not self.part_cycle_task.done():
            return

        self.part_cycle_task = asyncio.create_task(self.part_cycle_loop())

    async def stop_part_cycle(self) -> None:
        if self.part_cycle_task is None:
            return

        self.part_cycle_task.cancel()
        try:
            await self.part_cycle_task
        except asyncio.CancelledError:
            pass
        finally:
            self.part_cycle_task = None

    async def action_start(self) -> None:
        await self.safe_pulse("bStartCmd")
        await self.start_part_cycle()

    async def action_stop(self) -> None:
        await self.safe_pulse("bStopCmd")
        await self.stop_part_cycle()

    def action_quit(self) -> None:
        self.exit()

    async def on_shutdown(self) -> None:
        await self.stop_part_cycle()

        if self.monitor_task is not None:
            self.monitor_task.cancel()
            try:
                await self.monitor_task
            except asyncio.CancelledError:
                pass
