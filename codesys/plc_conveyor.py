import asyncio

from asyncua import Client

from .helpers import browse, monitor_signals, pulse, read_bool, write_bool
from .signal import Signal

IP = "192.168.6.218"
PORT = "4840"

URL = f"opc.tcp://{IP}:{PORT}"


async def run_test_sequence(
    start: Signal,
    stop: Signal,
    part_detected: Signal,
) -> None:
    await asyncio.sleep(1)

    print("\nStarting...")
    await pulse(start)

    await asyncio.sleep(2)

    for i in range(5):
        print(f"\nSensing part... {i + 1}")
        await pulse(part_detected)
        await asyncio.sleep(1)

    print("\nStopping...")
    await pulse(stop)

    await asyncio.sleep(1)


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

    monitor_task = None

    try:
        await client.connect()
        connected = True
        print("Connected\n")

        for signal in signals:
            await signal.set_node()
            # for debugging
            # print(f"{signal.name} -> {signal._node_id}")

        monitor_task = asyncio.create_task(
            monitor_signals(signals, interval=0.5))

        await run_test_sequence(
            start=start,
            stop=stop,
            part_detected=part_detected,
        )

    except asyncio.CancelledError:
        raise
    except Exception as exc:
        print(f"Connection error: {exc}")

    finally:
        if monitor_task is not None:
            monitor_task.cancel()
            try:
                await monitor_task
            except asyncio.CancelledError:
                pass

        if connected:
            print("Disconnecting")
            try:
                await client.disconnect()
            except Exception as exc:
                print(f"Disconnect warning: {exc}")
        print("Disconnected")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user (Ctrl + C)")
