import asyncio

from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis
from datetime import datetime

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

# from database import get_async_session, SessionLocal
from operations import init_currency_rate, update_currency_rate
from models import rate


app = FastAPI(
    title="tz_mobicult"
)


templates = Jinja2Templates(directory="templates")


@app.get("/")
def get_base_page(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


# @app.on_event("startup")
# async def startup():
#     with SessionLocal() as db:
#         res = db.execute(select(rate)).all()
#         if not res:
#             init_currency_rate(db)
#         else:
#             update_currency_rate(db)

    # redis = aioredis.from_url("redis://localhost")
    # FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
