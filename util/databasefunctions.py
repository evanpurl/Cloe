import os

import aiomysql
from aiomysql import Error
from dotenv import load_dotenv

load_dotenv()


async def create_pool():
    pool = await aiomysql.create_pool(host=os.getenv('host'), port=int(os.getenv('port')),
                                      user=os.getenv('user'), password=os.getenv('password'),
                                      db=os.getenv('db'))

    return pool


async def insert(pool, mysql):
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(mysql)
                await conn.commit()
        pool.close()
        await pool.wait_closed()
    except Error as e:
        print(e)


async def get(pool, mysql):
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(mysql)
                result = await cur.fetchone()

        pool.close()
        await pool.wait_closed()
        if not result:
            return 0
        if len(result) == 0:
            return 0
        return result[0]
    except Exception as e:
        print(e)


async def getall(pool, mysql):
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(mysql)
                result = await cur.fetchall()

        pool.close()
        await pool.wait_closed()
        if not result:
            return [0]
        if len(result) == 0:
            return [0]
        returnlist = []
        for a in result:
            returnlist.append(a[0])
        return returnlist
    except Exception as e:
        print(e)


async def createserver(pool, mysql):
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(mysql)
                await conn.commit()
        pool.close()
        await pool.wait_closed()
    except Exception as e:
        print(e)
        return e


async def deleteserver(pool, mysql):
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(mysql)
                await conn.commit()
        pool.close()
        await pool.wait_closed()
    except Exception as e:
        print(e)
        return e
