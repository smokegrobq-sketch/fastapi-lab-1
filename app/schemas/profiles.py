from pydantic import BaseModel, ConfigDict, Field


class ProfileBase(BaseModel):
    user_id: int
    phone: str = Field(min_length=5, max_length=30)
    address: str = Field(min_length=3, max_length=255)


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(BaseModel):
    phone: str | None = Field(default=None, min_length=5, max_length=30)
    address: str | None = Field(default=None, min_length=3, max_length=255)


class ProfileRead(ProfileBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
