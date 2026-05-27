from fastapi import APIRouter, HTTPException, status

from app.schemas.users import UserCreate, UserRead, UserUpdate
from app.storage.users import users_storage

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserRead])
def get_users() -> list[UserRead]:
    return list(users_storage.values())


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int) -> UserRead:
    user = users_storage.get(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate) -> UserRead:
    next_id = max(users_storage.keys(), default=0) + 1
    user = UserRead(id=next_id, **user_data.model_dump())
    users_storage[next_id] = user

    return user


@router.put("/{user_id}", response_model=UserRead)
def update_user(user_id: int, user_data: UserUpdate) -> UserRead:
    stored_user = users_storage.get(user_id)

    if stored_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    update_data = user_data.model_dump(exclude_unset=True)
    updated_user = stored_user.model_copy(update=update_data)
    users_storage[user_id] = updated_user

    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int) -> None:
    if user_id not in users_storage:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    del users_storage[user_id]
