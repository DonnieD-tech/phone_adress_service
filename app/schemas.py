from pydantic import BaseModel, Field


class PhoneCreate(BaseModel):
    phone: str = Field(
        ...,
        min_length=3,
        description='Номер телефона'
    )
    address: str = Field(
        ...,
        min_length=1,
        description='Адрес'
    )


class AddressUpdate(BaseModel):
    address: str = Field(
        ...,
        min_length=1,
        description='Новый адрес'
    )


class AddressOut(BaseModel):
    phone: str
    address: str