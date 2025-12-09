from fastapi import FastAPI, HTTPException, Depends, status, Response, Path
from fastapi.responses import JSONResponse
from app import schemas
from app.redis_client import get_redis
from app.utils import PHONE_PATTERN, PHONE_DESC, phone_normalization

app = FastAPI(
    title='phone-address-service',
    version='0.1'
)


@app.get('/phone/{phone}', response_model=schemas.AddressOut)
async def get_address(
        phone: str = Path(
            ...,
            pattern=PHONE_PATTERN,
            description=PHONE_DESC
        ),
        r = Depends(get_redis)
):
    key = phone_normalization(phone)
    address = await r.get(key)
    if address is None:
        raise HTTPException(
            status_code=404,
            detail='Телефон не найден'
        )
    return schemas.AddressOut(
        phone=phone,
        address=address
    )


@app.post('/phone', status_code=status.HTTP_201_CREATED)
async def create_phone(payload: schemas.PhoneCreate, r = Depends(get_redis)):
    key = phone_normalization(payload.phone)
    exists = await r.exists(key)
    if exists:
        raise HTTPException(
            status_code=409,
            detail='Телефон уже используется'
        )
    await r.set(key, payload.address)
    return JSONResponse(
        status_code=201,
        content={
            'phone': payload.phone,
            'address': payload.address
        }
    )


@app.put('/phone/{phone}', response_model=schemas.AddressOut)
async def update_phone(
        phone: str = Path(
            ...,
            pattern=PHONE_PATTERN,
            description=PHONE_DESC
        ),
        payload: schemas.AddressUpdate = ...,
        r = Depends(get_redis)
):
    key = phone_normalization(phone)
    exists = await r.exists(key)
    if not exists:
        raise HTTPException(
            status_code=404,
            detail='Телефон не найден'
        )
    await r.set(key, payload.address)
    return schemas.AddressOut(
        phone=phone,
        address=payload.address
    )


@app.delete('/phone/{phone}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_phone(phone: str = Path(
            ...,
            pattern=PHONE_PATTERN,
            description=PHONE_DESC
        ),
        r = Depends(get_redis)
):
    key = phone_normalization(phone)
    deleted = await r.delete(key)
    if deleted == 0:
        raise HTTPException(
            status_code=404,
            detail='Телефон не найден')

    return Response(status_code=204)