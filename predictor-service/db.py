# predictor-service/db.py
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

pool = None

async def init_db_pool():
    global pool
    pool = await asyncpg.create_pool(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT", 5432),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        min_size=2,
        max_size=10,
    )
    return pool

async def close_db_pool():
    global pool
    if pool:
        await pool.close()

async def get_state_coords(state_name: str):
    pool = get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT latitude, longitude FROM institutes WHERE state ILIKE $1",
            state_name
        )
        return row  # None if state not found

def get_pool():
    return pool