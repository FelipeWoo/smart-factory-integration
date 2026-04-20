import asyncio
from typing import Any, Awaitable, Callable

from pydantic import BaseModel, PrivateAttr


class Signal(BaseModel):
    name: str
    type: str
    state: bool = False
    _duration: float = 0.1
    _lock = asyncio.Lock()
    _task: asyncio.Task | None = None

    _node_id: str | None = PrivateAttr(default=None)
    _node: Any = PrivateAttr(default=None)
    _client: Any = PrivateAttr(default=None)
    _browse_fn: Callable[..., Awaitable[Any]
                         ] | None = PrivateAttr(default=None)
    _get_state_fn: Callable[..., Awaitable[Any]
                            ] | None = PrivateAttr(default=None)
    _set_state_fn: Callable[..., Awaitable[None]
                            ] | None = PrivateAttr(default=None)

    def bind_client(self, client: Any) -> None:
        self._client = client

    def bind_browse_fn(self, func: Callable[..., Awaitable[Any]]) -> None:
        self._browse_fn = func

    def bind_get_state_fn(self, func: Callable[..., Awaitable[Any]]) -> None:
        self._get_state_fn = func

    def bind_set_state_fn(self, func: Callable[..., Awaitable[None]]) -> None:
        self._set_state_fn = func

    async def set_node(self) -> None:
        if self._browse_fn is None:
            raise ValueError("browse function is not bound")
        self._node_id = await self._browse_fn(
            self.name, self._client.nodes.objects, 0, 10)

        if self._client is None:
            raise ValueError("client is not bound")

        if self._node_id is None:
            raise ValueError("node_id is not set")
        self._node = self._client.get_node(self._node_id)

    async def get_state(self) -> bool:
        if self._get_state_fn is None:
            raise ValueError("get_state function is not bound")

        if self._node is None:
            raise ValueError("node is not set")
        self.state = await self._get_state_fn(self._node)
        return self.state

    async def set_state(self, value: bool) -> None:
        if self._set_state_fn is None:
            raise ValueError("set_state function is not bound")
        if self._node is None:
            raise ValueError("node is not set")
        await self._set_state_fn(self._node, value)

    def pulse(self) -> None:
        if self._task is not None and not self._task.done():
            return

        self._task = asyncio.create_task(self._pulse())

    async def _pulse(self) -> None:
        async with self._lock:
            try:
                await self.set_state(True)
                await asyncio.sleep(self._duration)
                await self.set_state(False)
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                ValueError(f"Write error on {self.name}:\n{exc}")
            finally:
                self._task = None
