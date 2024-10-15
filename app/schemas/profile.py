from datetime import date

from pydantic import BaseModel, ConfigDict
from pydantic import Field

class ProfileBase(BaseModel):
    first_name: str | None = Field(default="", min_length=0, max_length=50000)
    last_name: str | None = Field(default="", min_length=0, max_length=50000)
    bio: str | None = Field(default="", min_length=0, max_length=50000)
    phone_number: str | None = Field(default="", min_length=0, max_length=50000)
    address: str | None = Field(default="", min_length=0, max_length=50000)
    date_of_birth: date | None = None


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(ProfileCreate):
    pass

class Profile(ProfileBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
