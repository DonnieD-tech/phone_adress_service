import pytest
import redis.asyncio as redis
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.redis_client import get_redis

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

@pytest.fixture(scope='module')
async def redis_client():
    r = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        decode_responses=True
    )
    await r.flushdb()
    yield r
    await r.flushdb()
    await r.close()


@pytest.mark.anyio
async def test_crud_flow(redis_client):
    app.dependency_overrides[get_redis] = lambda: redis_client

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://test') as ac:
        # GET not found
        r = await ac.get('/phone/123')
        assert r.status_code == 404


        # POST create
        r = await ac.post(
            '/phone',
            json={
                'phone': '123',
                'address': 'street 1'
            }
        )
        assert r.status_code == 201
        assert r.json()['address'] == 'street 1'


        # POST conflict
        r = await ac.post(
            '/phone',
            json={
                'phone': '123',
                'address': 'x'
            }
        )
        assert r.status_code == 409


        # GET found
        r = await ac.get('/phone/123')
        assert r.status_code == 200
        assert r.json()['address'] == 'street 1'


        # PUT update
        r = await ac.put(
            '/phone/123',
            json={
                'address': 'new street'
            }
        )
        assert r.status_code == 200
        assert r.json()['address'] == 'new street'


        # DELETE
        r = await ac.delete('/phone/123')
        assert r.status_code == 204


        # GET after delete -> 404
        r = await ac.get('/phone/123')
        assert r.status_code == 404