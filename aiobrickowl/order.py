import json

from enum import Enum
from typing import Dict
from typing import List
from typing import Union
from typing import Optional
from datetime import datetime
from dataclasses import dataclass

from aiobrickowl.bedding import ApiError
from aiobrickowl.session import ApiSession


OrderStatus = Enum(
    value = 'OrderStatus',
    names = [
        ('Pending',           0),
        ('Payment Submitted', 1),
        ('Payment Received',  2),
        ('Processing',        3),
        ('Processed',         4),
        ('Shipped',           5),
        ('Received',          6),
        ('On Hold',           7),
        ('Cancelled',         8),
    ],
)


OrderBaseCurrency = Enum(
    value = 'OrderBaseCurrency',
    names = [
        ('US Dollar', 'USD'),
    ]
)


@dataclass(frozen=True)
class Order:
    base_currency    : OrderBaseCurrency
    base_order_total : float
    order_date       : datetime
    order_id         : int
    status           : OrderStatus
    total_lots       : int
    total_quantity   : int
    url              : str

    @classmethod
    def from_dict(cls, source:Dict) -> 'Order':
        base_currency    = OrderBaseCurrency(source.get('base_currency'))
        base_order_total = float(source.get('base_order_total'))
        order_date       = datetime.utcfromtimestamp(int(source.get('order_date')))
        order_id         = int(source.get('order_id'))
        status           = OrderStatus[source.get('status')]
        total_lots       = int(source.get('total_lots'))
        total_quantity   = int(source.get('total_quantity'))
        url              = source.get('url')
        return Order(
            base_currency,
            base_order_total,
            order_date,
            order_id,
            status,
            total_lots,
            total_quantity,
            url,
        )


OrderListType = Enum(
    value = 'OrderListType',
    names = [
        ('Customer', 'customer'),
        #: Orders you have placed (as a Customer)
        ('Store',    'store'),
        #: Store Orders
    ],
)


@dataclass(frozen=True)
class OrderListParameters:
    status     : Optional[OrderStatus] = None
    #: Order status filter, use the formatted name or the numeric ID
    order_time : Optional[datetime] = None
    #: Unix Timestamp to limit the orders returned to those with a timestamp greater than or equal to the one provided.
    limit      : Optional[int] = None
    #: Limit the amount of results returned, defaults to 500.
    list_type  : Optional[OrderListType] = None
    #: Order list type

    def as_query_parameters(self) -> Dict[str, str]:
        query_parameters : Dict[str, str] = dict()
        if self.status:
            query_parameters.update({'status' : self.status.value})
        if self.order_time:
            query_parameters.update({'order_time' : self.order_time.timestamp()})
        if self.limit:
            query_parameters.update({'limit' : self.limit})
        if self.list_type:
            query_parameters.update({'list_type' : self.list_type.value})
        return query_parameters


async def list(session:ApiSession, parameters:OrderListParameters=None) -> Union[ApiError, List[Order]]:
    if not parameters:
        parameters = OrderListParameters()
    json_obj = await session.api_get('/order/list', parameters.as_query_parameters())
    return ApiError.from_dict(json_obj) or [ Order.from_dict(x) for x in json_obj ]
