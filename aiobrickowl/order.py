'''
    https://api.brickowl.com/v1/order/* API bindings.

    From BrickOwl's API Documentation:
    > The orders API allows you to download and process your stores orders and orders you have placed in stores.
'''

from enum import Enum
from typing import Dict
from typing import List
from typing import Union
from typing import Optional
from datetime import datetime
from dataclasses import dataclass

from aiobrickowl.bedding import Url
from aiobrickowl.bedding import ApiError
from aiobrickowl.session import ApiSession


OrderId = int
ColorId = int
ColorName = str
OrderItemId = int


OrderStatus = Enum( #pylint: disable=invalid-name
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


OrderBaseCurrency = Enum( #pylint: disable=invalid-name
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
    order_id         : OrderId
    status           : OrderStatus
    total_lots       : int
    total_quantity   : int
    url              : Url

    @classmethod
    def from_dict(cls, source:Dict) -> 'Order':
        base_currency    = OrderBaseCurrency(source.get('base_currency'))
        base_order_total = float(source.get('base_order_total'))
        order_date       = datetime.utcfromtimestamp(int(source.get('order_date')))
        order_id         = OrderId(source.get('order_id'))
        status           = OrderStatus[source.get('status')]
        total_lots       = int(source.get('total_lots'))
        total_quantity   = int(source.get('total_quantity'))
        url              = Url(source.get('url'))
        return cls(
            base_currency,
            base_order_total,
            order_date,
            order_id,
            status,
            total_lots,
            total_quantity,
            url,
        )


OrderListType = Enum( #pylint: disable=invalid-name
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
    ''' Get a list of your orders '''
    if not parameters:
        parameters = OrderListParameters()
    json_obj = await session.api_get('/order/list', parameters.as_query_parameters())
    return ApiError.from_dict(json_obj) or [ Order.from_dict(x) for x in json_obj ]


@dataclass(frozen=True)
class OrderItemTypedId:
    id   : str
    type : str

    @classmethod
    def from_dict(cls, source:Dict) -> 'OrderItemTypedId':
        id  = source.get('id')
        type = source.get('type')
        return cls(
            id,
            type,
        )


@dataclass(frozen=True)
class OrderItem:
    base_price       : float
    boid             : str
    color_id         : ColorId
    color_name       : ColorName
    condition        : str
    image_small      : Url
    lot_id           : int
    name             : str
    order_item_id    : OrderItemId
    ordered_quantity : int
    public_note      : str
    type             : str
    weight           : float
    ids              : List[OrderItemTypedId]

    @classmethod
    def from_dict(cls, source:Dict) -> 'OrderItem':
        base_price       = float(source.get('base_price'))
        boid             = source.get('boid')
        color_id         = ColorId(source.get('color_id'))
        color_name       = ColorName(source.get('color_name'))
        condition        = source.get('condition')
        image_small      = Url(source.get('image_small'))
        lot_id           = int(source.get('lot_id'))
        name             = source.get('name')
        order_item_id    = OrderItemId(source.get('order_item_id'))
        ordered_quantity = int(source.get('ordered_quantity'))
        public_note      = source.get('public_note')
        type             = source.get('type')
        weight           = float(source.get('weight'))
        ids              = [ OrderItemTypedId.from_dict(x) for x in source.get('ids')]
        return cls(
            base_price,
            boid,
            color_id,
            color_name,
            condition,
            image_small,
            lot_id,
            name,
            order_item_id,
            ordered_quantity,
            public_note,
            type,
            weight,
            ids,
        )


@dataclass(frozen=True)
class OrderItemsParameters:
    order_id : OrderId # The orders unique ID

    def as_query_parameters(self) -> Dict[str, str]:
        return {'order_id' : self.order_id}

async def items(session:ApiSession, parameters:OrderItemsParameters) -> Union[ApiError, List[OrderItem]]:
    ''' Retrieve order items '''
    json_obj = await session.api_get('/order/items', parameters.as_query_parameters())
    return ApiError.from_dict(json_obj) or [ OrderItem.from_dict(x) for x in json_obj ]
