import asyncio
from time import sleep

from asyncua import Client

from .helpers import browse, pulse, read_bool, state, write_bool
from .signal import Signal

IP = "192.168.6.218"
PORT = "4840"

URL = f"opc.tcp://{IP}:{PORT}"


async def main() -> None:

    print("Trying OPC anonymous connection...")

    client = Client(URL)
    connected = False

    signals = []

    lamp = Signal(name="lamp_on", type="boolean")
    signals.append(lamp)

    start = Signal(name="start_cmd", type="boolean")
    signals.append(start)

    stop = Signal(name="stop_cmd", type="boolean")
    signals.append(stop)

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

        sleep(.100)

        await state(signals)

        sleep(1)

        await pulse(start)
        await state(signals)

        sleep(5)

        await pulse(stop)
        await state(signals)

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
    asyncio.run(main())
