import asyncio

from asyncua import Client

from .dispatch_controller import DispatchController
from .helpers import browse, read_bool, write_bool
from .signal import Signal
from .signal_monitor import SignalMonitor
from .tui import PlcTui

IP = "192.168.6.218"
PORT = "4840"

URL = f"opc.tcp://{IP}:{PORT}"


async def main():
    print("Conveyor OPC anonymous connection...")

    client = Client(URL)
    connected = False

    signals = []

    start = Signal(name="bStartCmd", type="boolean")
    stop = Signal(name="bStopCmd", type="boolean")
    part_detected = Signal(name="bPartDetected", type="boolean")
    motor_running = Signal(name="bMotorIsRunning", type="boolean")
    system_ready = Signal(name="bSystemReady", type="boolean")

    signals.extend([
        start,
        stop,
        part_detected,
        motor_running,
        system_ready,
    ])

    for signal in signals:
        signal.bind_client(client)
        signal.bind_browse_fn(browse)
        signal.bind_get_state_fn(read_bool)
        signal.bind_set_state_fn(write_bool)

    try:
        await client.connect()
        connected = True
        print("Connected\n")

        for signal in signals:
            await signal.set_node()
            # for debugging
            # print(f"{signal.name} -> {signal._node_id}")

        dispatch_controller = DispatchController(
            part_signal=part_detected,
            auto_dispatch=True,
        )

        app = PlcTui(
            start_signal=start,
            stop_signal=stop,
            dispatch_controller=dispatch_controller,
        )

        monitor = SignalMonitor(
            signals=signals,
            ui_func=app.update_states,
            interval=0.3,
        )

        app.monitor = monitor

        await app.run_async()

    except asyncio.CancelledError:
        raise
    except Exception as exc:
        ValueError(f"Connection error: {exc}")

    finally:
        if connected:
            print("Disconnecting")
            try:
                await client.disconnect()
            except Exception as exc:
                ValueError(f"Disconnect warning: {exc}")
        print("Disconnected")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        ValueError("\nInterrupted by user (Ctrl + C)")
