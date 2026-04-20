from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Static

from .dispatch_controller import DispatchController
from .signal import Signal
from .signal_monitor import SignalMonitor


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
        ("r", "reset", "Reset"),
        ("q,escape", "quit", "Quit"),
    ]

    def __init__(
        self,
        start_signal: Signal,
        stop_signal: Signal,
        reset_signal: Signal,
        dispatch_controller: DispatchController,
        monitor: SignalMonitor | None = None,
    ) -> None:
        super().__init__()
        self.start_signal = start_signal
        self.stop_signal = stop_signal
        self.reset_signal = reset_signal
        self.dispatch_controller = dispatch_controller
        self.monitor = monitor

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Connecting...", id="states")
        yield Footer()

    async def update_states(self, lines: list[str]) -> None:
        self.query_one("#states", Static).update("\n".join(lines))

    async def action_start(self) -> None:
        self.start_signal.pulse()
        self.dispatch_controller.start()

    async def action_stop(self) -> None:
        self.stop_signal.pulse()
        await self.dispatch_controller.stop()

    async def action_reset(self) -> None:
        self.reset_signal.pulse()

    async def action_quit(self) -> None:
        if self.monitor is not None:
            await self.monitor.stop()
        self.exit()

    async def on_mount(self) -> None:
        if self.monitor is not None:
            self.monitor.start()

    async def on_shutdown(self) -> None:
        await self.dispatch_controller.stop()
        if self.monitor is not None:
            await self.monitor.stop()
