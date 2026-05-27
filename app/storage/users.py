from app.schemas.users import UserRead

users_storage: dict[int, UserRead] = {
    1: UserRead(id=1, name="Alice Johnson", email="alice@example.com", age=25),
    2: UserRead(id=2, name="Bob Smith", email="bob@example.com", age=31),
}
