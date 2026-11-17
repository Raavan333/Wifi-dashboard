from typing import Optional

import asyncpg

from app.config import get_settings


class Database:
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None

    async def fetchdict(
        self,
        query: str,
        *args,
    ):
        rows = await self.fetch(query, *args)

        return [
            dict(row)
            for row in rows
        ]
    

    async def fetchrowdict(
        self,
        query: str,
        *args,
    ):
        row = await self.fetchrow(query, *args)

        if not row:
            return None

        return dict(row)

    async def connect(self) -> None:
        settings = get_settings()

        self.pool = await asyncpg.create_pool(
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
            database=settings.POSTGRES_DB,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASS,
            min_size=settings.DB_MIN_CONNECTIONS,
            max_size=settings.DB_MAX_CONNECTIONS,
            command_timeout=settings.QUERY_TIMEOUT_SECONDS,
        )

    async def disconnect(self) -> None:
        if self.pool:
            await self.pool.close()

    # async def fetch(
    #     self,
    #     query: str,
    #     *args,
    # ):
    #     async with self.pool.acquire() as conn:
    #         return await conn.fetch(query, *args)

    async def fetch(
        self,
        query: str,
        *args,
    ):

        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)

    async def fetchrow(
        self,
        query: str,
        *args,
    ):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, *args)

    async def fetchval(
        self,
        query: str,
        *args,
    ):
        async with self.pool.acquire() as conn:
            return await conn.fetchval(query, *args)

    async def execute(
        self,
        query: str,
        *args,
    ):
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)


db = Database()