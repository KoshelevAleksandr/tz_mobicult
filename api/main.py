import asyncio
from typing import List

from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis
from datetime import datetime

from routers import router as test_router

from schemas import Rate

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session, SessionLocal
from operations import init_currency_rate, startup_update_currency_rate, get_currency_rate_before_yesterday, \
    get_currency_rate_yesterday, get_currency_rate_today
from models import rate


app = FastAPI(
    title="tz_mobicult"
)

# with SessionLocal() as db:
#     res = db.execute(select(rate)).all()
#     if not res:
#         init_currency_rate(db)
#     else:
#         update_currency_rate(db)

templates = Jinja2Templates(directory="templates")


app.include_router(test_router)


@app.get("/")
def get_base_page(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})





@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


