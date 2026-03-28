import time

from pymodbus.client import ModbusTcpClient


def state(client: ModbusTcpClient) -> None:
    print(50*"*")
    keys = ["led", "coil", "start", "stop"]
    result = client.read_coils(address=0, count=4)
    if result.isError():
        print("Error:", result)
    else:
        data = dict(zip(keys, result.bits))
        for k, v in data.items():
            print(f"{k}: {v}")
    print(50*"*")


def main():

    client = ModbusTcpClient("localhost", port=502)

    ok = client.connect()
    print("connected:", ok)

    # led (%QX0.0) = (address=0, count=8)
    # coil (%QX0.1) = (address=1, count=8)
    # start_cmd (%QX0.2) = (address=0, count=8)
    # stop_cmd (%QX0.3) = (address=1, count=8)
    print("idle")
    state(client)
    time.sleep(0.1)
    # start_cmd
    print("starting...")
    client.write_coil(address=2, value=True)
    time.sleep(1)
    state(client)
    print("resetting start...")
    client.write_coil(address=2, value=False)
    time.sleep(5)
    # stop_cmd
    print("stopping...")
    client.write_coil(address=3, value=True)
    time.sleep(1)
    state(client)
    time.sleep(5)
    print("resetting stop...")
    client.write_coil(address=3, value=False)
    time.sleep(1)
    state(client)

    client.close()


if __name__ == "__main__":
    main()
