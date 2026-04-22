from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Order(_message.Message):
    __slots__ = ("id", "items", "description", "price", "destination")
    ID_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_FIELD_NUMBER: _ClassVar[int]
    id: str
    items: _containers.RepeatedScalarFieldContainer[str]
    description: str
    price: float
    destination: str
    def __init__(self, id: _Optional[str] = ..., items: _Optional[_Iterable[str]] = ..., description: _Optional[str] = ..., price: _Optional[float] = ..., destination: _Optional[str] = ...) -> None: ...

class CombinedShipment(_message.Message):
    __slots__ = ("id", "status", "orders")
    ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ORDERS_FIELD_NUMBER: _ClassVar[int]
    id: str
    status: str
    orders: _containers.RepeatedCompositeFieldContainer[Order]
    def __init__(self, id: _Optional[str] = ..., status: _Optional[str] = ..., orders: _Optional[_Iterable[_Union[Order, _Mapping]]] = ...) -> None: ...

class StringMessage(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: str
    def __init__(self, value: _Optional[str] = ...) -> None: ...
