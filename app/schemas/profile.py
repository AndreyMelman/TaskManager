import re
from datetime import date, datetime
from email.policy import default
from typing import Any
from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field, field_validator
from annotated_types import MaxLen, MinLen


class ProfileBase(BaseModel):
    first_name: str | None = Field(default=None, max_length=50)
    last_name: str | None = Field(default=None, max_length=50)
    bio: str | None = Field(default=None, min_length=0, max_length=50000)
    phone_number: str | None = Field(default=None)
    address: str | None = Field(default=None, min_length=0, max_length=500)
    date_of_birth: date | None = Field(default=None, validate_default=True)

    @field_validator("phone_number")
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
