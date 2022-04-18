import asyncio
import asyncpg

from uuid import uuid4
from faker import Faker
from random import randint


async def table_exists(conn):
    result = await conn.fetchrow(
        """
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = 'test'
        LIMIT 1;
        """
    )
    return result[0] > 0


async def create_table_if_needed(conn):
    if not await table_exists(conn):
        await conn.execute(
            """
            CREATE TABLE test (
                id serial PRIMARY KEY, num INT, long_string VARCHAR, date_ DATE
                );
            """
        )


async def run():
    conn = await asyncpg.connect(
        host="host.docker.internal",
        database="postgres",
        user="postgres",
        password="example",
    )

    async with conn.transaction():
        fake = Faker()

        await create_table_if_needed(conn)

        values = [f"({randint(1, 10000)}, '{uuid4()}', ${i+1})" for i in range(5000)]

        await conn.execute(
            f"""
            INSERT INTO test (num, long_string, date_)
            VALUES {(", ").join(values)};
            """,
            *[
                fake.date_between(start_date="today", end_date="+30y")
                for _ in range(5000)
            ],
        )

        print(f"Inserted {len(values)} rows in the db.")

    await conn.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    loop.close()
