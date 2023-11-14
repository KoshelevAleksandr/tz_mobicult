from celery import Celery
from celery.schedules import crontab
from fastapi import Depends
from sqlalchemy import select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession

from operations import get_currency_rate_today, get_currency_rate_yesterday, get_currency_rate_before_yesterday, \
    init_currency_rate
from database import get_async_session, SessionLocal

from models import rate

celery_app = Celery('tasks', broker='redis://localhost:6379')

celery_app.conf.timezone = 'Europe/Moscow'


# @celery_app.task
# def get_celery_rate():
#     with SessionLocal() as db:
#         # init_currency_rate(db)
#
#         today = get_currency_rate_today()
#         yesterday_rate = get_currency_rate_yesterday()
#         before_yesterday_rate = get_currency_rate_before_yesterday()
#         stmt_usd = insert(rate).values(
#             currency='USD',
#             today=today['USD'],
#             yesterday=yesterday_rate['USD'],
#             before_yesterday=before_yesterday_rate['USD'])
#         stmt_eur = insert(rate).values(
#             currency='EUR',
#             today=today['EUR'],
#             yesterday=yesterday_rate['EUR'],
#             before_yesterday=before_yesterday_rate['EUR'])
#         db.execute(stmt_usd)
#         db.execute(stmt_eur)
#         db.commit()
#         print({"status": "success"})




@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s('hello'))

    # Calls test('hello') every 30 seconds.
    # It uses the same signature of previous task, an explicit name is
    # defined to avoid this task replacing the previous one defined.
    # sender.add_periodic_task(30.0, test.s('hello'), name='add every 30')

    # sender.add_periodic_task(30.0, test.s('world'), expires=10)
    #
    # sender.add_periodic_task(
    #     crontab(hour=7, minute=30, day_of_week=1),
    #     test.s('Happy Mondays!'),
    # )


@celery_app.task
def test(arg):
    print(arg)




