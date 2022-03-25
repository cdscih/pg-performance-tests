from fastapi import FastAPI
import asyncpg

import uvicorn

pool = None


async def get_pool():
    global pool
    if not pool:
        pool = await asyncpg.create_pool(
            host="db", database="postgres", user="postgres", password="example"
        )
    return pool


async def connection_pool_handler():
    pool = await get_pool()
    async with pool.acquire() as con:
        records = await con.fetch("SELECT * from test")
        return {"fetched_records_length": len(records)}


async def single_connection_handler():
    con = await asyncpg.connect(
        host="db", database="postgres", user="postgres", password="example"
    )
    records = await con.fetch("SELECT * from test")
    con.close()
    return {"fetched_records_length": len(records)}


def create_app():
    app = FastAPI()
    app.add_api_route("/", connection_pool_handler, methods=["GET"])
    app.add_api_route("/connection_pool", connection_pool_handler, methods=["GET"])
    app.add_api_route(
        "/single_connection", single_connection_handler, methods=["GET"]
    )
    return app


app = create_app()

uvicorn.run(app, host="0.0.0.0", port=8000)
