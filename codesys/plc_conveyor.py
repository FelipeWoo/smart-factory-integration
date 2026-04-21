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

    start = Signal(name="bStartCmd", type="io")
    stop = Signal(name="bStopCmd", type="io")
    reset = Signal(name="bResetCmd", type="io")

    system_ready = Signal(name="bSystemReady", type="state")
    auto_mode = Signal(name="bAutoMode", type="state")
    alarm = Signal(name="bAlarmActive", type="state")

    part_detected_1 = Signal(name="bPartDetected_1", type="io")
    conveyor_jam_1 = Signal(name="bConveyorJam_1", type="state")
    conveyor_starvation_1 = Signal(name="bConveyorStarvation_1", type="state")
    motor_running_1 = Signal(name="bConveyorMotorIsRunning_1", type="state")

    signals.extend([
        start,
        stop,
        reset,

        system_ready,
        auto_mode,
        alarm,

        part_detected_1,
        conveyor_jam_1,
        conveyor_starvation_1,
        motor_running_1,
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
            part_signal=part_detected_1,
            auto_dispatch=True,
        )

        app = PlcTui(
            start_signal=start,
            stop_signal=stop,
            reset_signal=reset,
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
        raise ValueError(f"Connection error: {exc}")

    finally:
        if connected:
            print("Disconnecting")
            try:
                await client.disconnect()
            except Exception as exc:
                raise ValueError(f"Disconnect warning: {exc}")
        print("Disconnected")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        raise ValueError("\nInterrupted by user (Ctrl + C)")
