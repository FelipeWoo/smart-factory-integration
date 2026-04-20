import asyncio
from asyncio import sleep

from asyncua import Client

from .helpers import browse, pulse, read_bool, state, write_bool
from .signal import Signal

IP = "192.168.6.218"
PORT = "4840"

URL = f"opc.tcp://{IP}:{PORT}"


async def main():
    print("Conveyor OPC anonymous connection...")

    client = Client(URL)
    connected = False

    signals = []

    start = Signal(name="bStartCmd", type="boolean")
    signals.append(start)

    stop = Signal(name="bStopCmd", type="boolean")
    signals.append(stop)

    part_detected = Signal(name="bPartDetected", type="boolean")
    signals.append(part_detected)

    motor_running = Signal(name="bMotorIsRunning", type="boolean")
    signals.append(motor_running)

    system_ready = Signal(name="bSystemReady", type="boolean")
    signals.append(system_ready)

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
        print()

        await sleep(.100)

        await state(signals)

        await sleep(1)

        print("Starting...")
        await pulse(start)
        await state(signals)

        for _ in range(10):
            print("Sensing part...")
            await pulse(part_detected)
            await sleep(1)

        print("Stopping...")
        await pulse(stop)
        await state(signals)

    except asyncio.CancelledError:
        raise
    except Exception as exc:
        print(f"Connection error: {exc}")

    finally:
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
