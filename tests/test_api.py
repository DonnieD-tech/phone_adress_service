import pytest
import redis.asyncio as redis
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.redis_client import get_redis


REDIS_HOST = 'localhost'
REDIS_PORT = 6379


class FakeRedis:
    def __init__(self):
        self.data = {}

    async def get(self, key):
        return self.data.get(key)

    async def set(self, key, value):
        self.data[key] = value

    async def exists(self, key):
        return key in self.data

    async def delete(self, key):
        self.data.pop(key, None)

    async def flushdb(self):
        self.data.clear()

    async def aclose(self):
        pass


@pytest.fixture(scope="module")
async def redis_client():
    r = FakeRedis()
    await r.flushdb()
    yield r
    await r.flushdb()


@pytest.mark.anyio
async def test_crud_flow(redis_client):
    app.dependency_overrides[get_redis] = lambda: redis_client

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://test') as ac:
        phone = "+79399562637"  # валидный номер

        # GET not found
        r = await ac.get(f'/phone/{phone}')
        assert r.status_code == 404

        # POST create
        r = await ac.post(
            '/phone',
            json={
                'phone': phone,
                'address': 'street 1'
            }
        )
        assert r.status_code == 201
        assert r.json()['address'] == 'street 1'

        # POST conflict
        r = await ac.post(
            '/phone',
            json={
                'phone': phone,
                'address': 'x'
            }
        )
        assert r.status_code == 409

        # GET found
        r = await ac.get(f'/phone/{phone}')
        assert r.status_code == 200
        assert r.json()['address'] == 'street 1'

        # PUT update
        r = await ac.put(
            f'/phone/{phone}',
            json={'address': 'new street'}
        )
        assert r.status_code == 200
        assert r.json()['address'] == 'new street'

        # DELETE
        r = await ac.delete(f'/phone/{phone}')
        assert r.status_code == 204

        # GET after delete -> 404
        r = await ac.get(f'/phone/{phone}')
        assert r.status_code == 404