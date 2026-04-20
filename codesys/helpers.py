from asyncio import sleep
from typing import Any, List

from .signal import Signal


async def read_bool(node) -> bool:
    value = await node.read_value()
    return value


async def write_bool(node: Any, value: bool) -> None:
    await node.write_value(value)


async def browse(name: str, node: Any, level: int = 0, max_depth: int = 4) -> Any:
    if level > max_depth:
        return None

    try:
        browse_name = await node.read_browse_name()
        node_id = node.nodeid.to_string()

    except Exception as exc:
        print(f"{'  ' * level}- error: {exc}")
        return None

    clean_name = str(browse_name).split("'")[1]

    if name == clean_name:
        return node_id

    try:
        children = await node.get_children()
    except Exception:
        return None

    for child in children:
        result = await browse(name, child, level + 1, max_depth)
        if result is not None:
            return result

    return None


async def state(signals: List[Signal]) -> None:
    for signal in signals:
        await signal.get_state()
        print(signal)
    print()


async def pulse(signal: Signal) -> None:
    await signal.set_state(True)
    await sleep(.500)
    await signal.set_state(False)


async def monitor_signals(signals: list[Signal], interval: float = 0.5) -> None:
    while True:
        print("\n--- STATES ---")
        for signal in signals:
            value = await signal.get_state()
            print(f"{signal.name}: {value}")
        await sleep(interval)
