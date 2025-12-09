from pydantic import BaseModel, Field, constr
from app.utils import PHONE_PATTERN, PHONE_EXAMPLES, ADDRESS_EXAMPLES, PHONE_DESC, ADDRESS_DESC


class PhoneCreate(BaseModel):
    phone: constr(pattern=PHONE_PATTERN) = Field(
        ...,
        examples=PHONE_EXAMPLES,
        description=PHONE_DESC
    )
    address: str = Field(
        ...,
        examples=ADDRESS_EXAMPLES,
        description=ADDRESS_DESC
    )


class AddressUpdate(BaseModel):
    address: str = Field(
        ...,
        examples=ADDRESS_EXAMPLES,
        description='Новый адрес'
    )


class AddressOut(BaseModel):
    phone: str = Field(
        ...,
        examples=PHONE_EXAMPLES,
        description=PHONE_DESC
    )
    address: str = Field(
        ...,
        examples=ADDRESS_EXAMPLES,
        description=ADDRESS_DESC
    )