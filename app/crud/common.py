from typing import Any, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

ModelT = TypeVar("ModelT")


async def get_one(session: AsyncSession, model: type[ModelT], item_id: int) -> ModelT | None:
    return await session.get(model, item_id)


async def get_many(session: AsyncSession, model: type[ModelT]) -> list[ModelT]:
    result = await session.execute(select(model).order_by(model.id))
    return list(result.scalars().all())


async def create_one(session: AsyncSession, model: type[ModelT], data: dict[str, Any]) -> ModelT:
    item = model(**data)
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item


async def update_one(item: Any, session: AsyncSession, data: dict[str, Any]) -> Any:
    for key, value in data.items():
        setattr(item, key, value)

    await session.commit()
    await session.refresh(item)
    return item


async def delete_one(session: AsyncSession, item: Any) -> None:
    await session.delete(item)
    await session.commit()
