from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.dependencies import get_current_user
from app.db.session import get_session
from app.models.order import Order
from app.models.profile import Profile
from app.models.user import User
from app.schemas.orders import OrderRead
from app.schemas.profiles import ProfileRead
from app.schemas.users import UserRead

router = APIRouter(prefix="/me", tags=["me"])


@router.get("/", response_model=UserRead)
async def get_me(current_user: User = Depends(get_current_user)) -> User:
    return current_user


@router.get("/profile", response_model=ProfileRead | None)
async def get_my_profile(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> Profile | None:
    result = await session.execute(
        select(Profile).where(Profile.user_id == current_user.id)
    )
    return result.scalar_one_or_none()


@router.get("/orders", response_model=list[OrderRead])
async def get_my_orders(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> list[Order]:
    result = await session.execute(
        select(Order)
        .options(selectinload(Order.items))
        .where(Order.user_id == current_user.id)
        .order_by(Order.id)
    )
    return list(result.scalars().all())
