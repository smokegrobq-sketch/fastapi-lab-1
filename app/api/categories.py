from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.common import create_one, delete_one, get_many, get_one, update_one
from app.db.session import get_session
from app.models.category import Category
from app.schemas.categories import CategoryCreate, CategoryRead, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=list[CategoryRead])
async def get_categories(session: AsyncSession = Depends(get_session)) -> list[Category]:
    return await get_many(session, Category)


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: CategoryCreate,
    session: AsyncSession = Depends(get_session),
) -> Category:
    return await create_one(session, Category, category_data.model_dump())


@router.put("/{category_id}", response_model=CategoryRead)
async def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    session: AsyncSession = Depends(get_session),
) -> Category:
    category = await get_one(session, Category, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return await update_one(category, session, category_data.model_dump(exclude_unset=True))


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    session: AsyncSession = Depends(get_session),
) -> None:
    category = await get_one(session, Category, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    await delete_one(session, category)
