from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.common import create_one, delete_one, get_many, get_one, update_one
from app.db.session import get_session
from app.models.product import Product
from app.schemas.products import ProductCreate, ProductRead, ProductUpdate

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=list[ProductRead])
async def get_products(session: AsyncSession = Depends(get_session)) -> list[Product]:
    return await get_many(session, Product)


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    session: AsyncSession = Depends(get_session),
) -> Product:
    return await create_one(session, Product, product_data.model_dump())


@router.put("/{product_id}", response_model=ProductRead)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    session: AsyncSession = Depends(get_session),
) -> Product:
    product = await get_one(session, Product, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return await update_one(product, session, product_data.model_dump(exclude_unset=True))


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    session: AsyncSession = Depends(get_session),
) -> None:
    product = await get_one(session, Product, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    await delete_one(session, product)
