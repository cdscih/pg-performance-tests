import asyncio
import asyncpg

from uuid import uuid4


async def table_exists(conn):
    result = await conn.fetchrow(
        "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'test'"  # noqa: E501
    )
    return result[0] > 0


async def create_table_if_needed(conn):
    if not await table_exists(conn):
        await conn.execute(
            "CREATE TABLE test (id serial PRIMARY KEY, num varchar, data varchar, other_data varchar, even_more_data varchar);"  # noqa: E501
        )


async def run():
    conn = await asyncpg.connect(
        host="host.docker.internal",
        database="postgres",
        user="postgres",
        password="example",
    )

    async with conn.transaction():

        await create_table_if_needed(conn)

        for i in range(5000):
            num, data, other_data, even_more_data = (
                uuid4(),
                uuid4(),
                uuid4(),
                uuid4(),
            )
            await conn.execute(
                f"INSERT INTO test (num, data, other_data, even_more_data) VALUES ('{num}', '{data}', '{other_data}', '{even_more_data}')"  # noqa: E501
            )
            print(
                f"row {i+1} inserted {num}, {data}, {other_data}, {even_more_data}"  # noqa: E501
            )

    await conn.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    loop.close()
