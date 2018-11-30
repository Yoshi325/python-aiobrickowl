from types import TracebackType
from typing import Dict
from typing import Type
from typing import Optional
from functools import partial

import aiohttp


class ApiSession:
    def __init__(self, api_key:str):
        self._api_key = api_key
        self._aio_http_client_session = aiohttp.ClientSession()

    async def api_get(self, path:str, params:Dict[str, str]=None):
        if not params:
            params = dict()
        params.update({'key' : self._api_key})
        path = path.lstrip('/')
        _get = partial(
            self._aio_http_client_session.get,
            f'https://api.brickowl.com/v1/{path}',
            params=params,
        )
        async with _get() as response:
            return await response.json()

    async def close(self) -> None:
        await self._aio_http_client_session.close()

    def __enter__(self):
        raise TypeError("Please use `async with` instead.")

    def __exit__(self, exc_type, exc_val, exc_tb):
        # __exit__ should exist in pair with __enter__ but never executed
        pass

    async def __aenter__(self) -> 'ApiSession':
        return self

    async def __aexit__(self, exc_type: Optional[Type[BaseException]], exc_val: Optional[BaseException], exc_tb: Optional[TracebackType]) -> None:
        await self.close()
