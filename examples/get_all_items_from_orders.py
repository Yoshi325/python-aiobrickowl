#pylint: disable=wrong-import-position
'''
    An example of how to use aiobrickowl to return all items from your (as a customer) orders.
'''

import os
import sys
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio


from aiobrickowl.session import ApiSession
from aiobrickowl.shortcuts import order_items
from aiobrickowl.shortcuts import order_list_customer


async def main(api_key:str): #pylint: disable=missing-docstring
    async with ApiSession(api_key) as session:

        orders = await order_list_customer(session)
        for order_ in orders:
            print('order:', order_.order_id)
            items = await order_items(session, order_.order_id)
            # another way to accomplish this is:
            # from aiobrickowl import order
            # items = await order.items(session, order_.order_id)
            for item in items:
                print(item)

if ('__main__' == __name__): #pylint: disable=missing-docstring
    _api_key = os.environ.get('BRICKOWL_API_KEY') #pylint: disable=invalid-name
    if not _api_key:
        print('Error! Please set your BrickOwl Api Key as an environment variable named: BRICKOWL_API_KEY.')
        sys.exit(1)
    else:
        event_loop = asyncio.get_event_loop() #pylint: disable=invalid-name
        event_loop.run_until_complete(main(_api_key))
        sys.exit(0)
