from typing import List
from typing import Union
from functools import partial

from aiobrickowl import order
from aiobrickowl.order import OrderId
from aiobrickowl.order import OrderItem
from aiobrickowl.order import OrderListType
from aiobrickowl.order import OrderListParameters
from aiobrickowl.order import OrderItemsParameters
from aiobrickowl.bedding import ApiError
from aiobrickowl.session import ApiSession


order_list_customer = partial(
    order.list,
    parameters=OrderListParameters(list_type=OrderListType['Customer'])
)


async def order_items(session:ApiSession, order_id:OrderId) -> Union[ApiError, List[OrderItem]]:
    return await order.items(session, OrderItemsParameters(order_id))
