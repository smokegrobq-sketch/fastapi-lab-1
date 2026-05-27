from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.common import create_one, delete_one, get_many, get_one, update_one
from app.db.session import get_session
from app.models.profile import Profile
from app.schemas.profiles import ProfileCreate, ProfileRead, ProfileUpdate

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.get("/", response_model=list[ProfileRead])
async def get_profiles(session: AsyncSession = Depends(get_session)) -> list[Profile]:
    return await get_many(session, Profile)


@router.post("/", response_model=ProfileRead, status_code=status.HTTP_201_CREATED)
async def create_profile(
    profile_data: ProfileCreate,
    session: AsyncSession = Depends(get_session),
) -> Profile:
    return await create_one(session, Profile, profile_data.model_dump())


@router.put("/{profile_id}", response_model=ProfileRead)
async def update_profile(
    profile_id: int,
    profile_data: ProfileUpdate,
    session: AsyncSession = Depends(get_session),
) -> Profile:
    profile = await get_one(session, Profile, profile_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return await update_one(profile, session, profile_data.model_dump(exclude_unset=True))


@router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(
    profile_id: int,
    session: AsyncSession = Depends(get_session),
) -> None:
    profile = await get_one(session, Profile, profile_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    await delete_one(session, profile)
