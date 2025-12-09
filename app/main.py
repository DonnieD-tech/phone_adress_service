from fastapi import FastAPI, HTTPException, Depends, status, Response
from fastapi.responses import JSONResponse
from app import schemas
from app.redis_client import get_redis

app = FastAPI(title='phone-address-service')


KEY_PREFIX = 'phone:'


def make_key(phone: str) -> str:
    return f"{KEY_PREFIX}{phone}"


@app.get('/phone/{phone}', response_model=schemas.AddressOut)
async def get_address(phone: str, r = Depends(get_redis)):
    key = make_key(phone)
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
    key = make_key(payload.phone)
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
async def update_phone(phone: str, payload: schemas.AddressUpdate, r = Depends(get_redis)):
    key = make_key(phone)
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
async def delete_phone(phone: str, r = Depends(get_redis)):
    key = make_key(phone)
    deleted = await r.delete(key)
    if deleted == 0:
        raise HTTPException(
            status_code=404,
            detail='Телефон не найден')

    return Response(status_code=204)