from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.common import delete_one, get_one, update_one
from app.db.session import get_session
from app.models.order import Order
from app.models.order_item import OrderItem
from app.schemas.orders import OrderCreate, OrderRead, OrderUpdate

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/", response_model=list[OrderRead])
async def get_orders(session: AsyncSession = Depends(get_session)) -> list[Order]:
    result = await session.execute(
        select(Order).options(selectinload(Order.items)).order_by(Order.id)
    )
    return list(result.scalars().all())


@router.post("/", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: OrderCreate,
    session: AsyncSession = Depends(get_session),
) -> Order:
    payload = order_data.model_dump()
    items = payload.pop("items", [])
    order = Order(**payload)
    order.items = [OrderItem(**item) for item in items]
    session.add(order)
    await session.commit()

    result = await session.execute(
        select(Order).options(selectinload(Order.items)).where(Order.id == order.id)
    )
    return result.scalar_one()


@router.put("/{order_id}", response_model=OrderRead)
async def update_order(
    order_id: int,
    order_data: OrderUpdate,
    session: AsyncSession = Depends(get_session),
) -> Order:
    order = await get_one(session, Order, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    await update_one(order, session, order_data.model_dump(exclude_unset=True))

    result = await session.execute(
        select(Order).options(selectinload(Order.items)).where(Order.id == order_id)
    )
    return result.scalar_one()


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(
    order_id: int,
    session: AsyncSession = Depends(get_session),
) -> None:
    order = await get_one(session, Order, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    await delete_one(session, order)
