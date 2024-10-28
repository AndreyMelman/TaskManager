import re

from datetime import date, datetime
from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProfileBase(BaseModel):
    first_name: Annotated[str | None, Field(max_length=50)] = None
    last_name: Annotated[str | None, Field(max_length=50)] = None
    bio: Annotated[str | None, Field(max_length=500)] = None
    phone_number: str | None = Field(default=None)
    address: Annotated[str | None, Field(max_length=500)] = None
    date_of_birth: Annotated[date | None, Field(validate_default=True)] = None

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str) -> str:
        if not re.match(r"^\+\d{1,15}$", value):
            raise ValueError(
                'Номер телефона должен начинаться с "+" и содержать от 1 до 15 цифр'
            )
        return value

    @field_validator("date_of_birth")
    @classmethod
    def validate_date_of_birth(cls, values: date) -> date:
        if values and values >= datetime.now().date():
            raise ValueError("Дата рождения должна быть в прошлом")
        return values


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(ProfileCreate):
    pass


class Profile(ProfileBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
