import os
import sys
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio

from aiobrickowl import order
from aiobrickowl.order import OrderListType
from aiobrickowl.order import OrderListParameters
from aiobrickowl.session import ApiSession


async def main(api_key:str):
    async with ApiSession(api_key) as session:
        response = await order.list(session, OrderListParameters(list_type=OrderListType['Customer']))
        print(response)

if ('__main__' == __name__):
    _api_key = os.environ.get('BRICKOWL_API_KEY')
    if not _api_key:
        print('Error! Please set your BrickOwl Api Key as an environment variable named: BRICKOWL_API_KEY.')
        sys.exit(1)
    else:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(_api_key))
        sys.exit(0)
