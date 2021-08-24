from app.models import (
    Product,
    User,
    UserPushToken,
    Order,
    order_item_pydantic,
    order_item_pydanticIn,
    order_pydantic,
    OrderItem,
    product_pydantic,
)

from fastapi import HTTPException, status
from datetime import datetime

from pydantic import BaseModel

from typing import List


class OrderItemOut(BaseModel):
    id: str
    price: float
    quantity: int
    product: product_pydantic


class OrderOut(BaseModel):
    id: int
    receiver_name: str
    receiver_phone_number: str
    receiver_street_address: str
    receiver_city: str
    receiver_state: str
    amount: float
    payment_ref_id: str
    created_at: datetime
    status: str
    items: List[OrderItemOut]


async def get_orders(skip: int = 0, limit: int = 100):
    orders = (
        await Order.all()
        .limit(limit)
        .offset(skip)
        .order_by("-created_at")
    )
    return orders


async def set_order_delivered(order_id: int):
    order = await Order.get_or_none(id=order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Order with id {order_id} doesn't exists",
        )
    await Order.filter(id=order_id).update(
        status="DELIVERED"
    )
    return order


async def get_all_pending_orders(
    skip: int = 0, limit: int = 100
):
    orders = (
        await Order.filter(status="PAID")
        .all()
        .limit(limit)
        .offset(skip)
        .order_by("-created_at")
    )
    return orders


async def get_order_id(id: int):
    order_details = (
        await order_pydantic.from_queryset_single(
            Order.get(id=id)
        )
    )
    order_details = order_details.dict()
    items = await OrderItem.filter(order_id=id).all()
    new_items = []
    for item in items:
        item_details = (
            await order_item_pydantic.from_queryset_single(
                OrderItem.get(id=item.id)
            )
        )
        item_details = item_details.dict()
        product = await Product.get(id=item.product_id)
        item_details.update({"product": product})
        # print(product)
        new_items.append(item_details)
    order_details.update({"items": new_items})
    return order_details
