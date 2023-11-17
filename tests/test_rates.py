import pytest
from sqlalchemy import update, select, insert
from fastapi.testclient import TestClient

from api.main import app
from api.models import rate
from api.operations import init_currency_rate
from conftest import SessionLocal_test


def test_init_rate():
    with SessionLocal_test() as session:
        init_currency_rate(session)
        query = select(rate)
        result = session.execute(query)
        assert result.all() != [], "Курс валют не добавлен"


def test_update_rate():
    with SessionLocal_test() as session:
        stmt_usd = update(rate).values(
            currency='USD',
            today=1,
            yesterday=2,
            before_yesterday=3).where(rate.c.currency == 'USD')
        stmt_eur = update(rate).values(
            currency='EUR',
            today=1,
            yesterday=2,
            before_yesterday=3).where(rate.c.currency == 'EUR')
        session.execute(stmt_usd)
        session.execute(stmt_eur)
        session.commit()

        query = select(rate)
        result = session.execute(query)
        assert result.all() == [(1, 'USD', 1.0, 2.0, 3.0), (2, 'EUR', 1.0, 2.0, 3.0)], "Курс валют не обновился"


async def test_get_rates():
    with TestClient(app) as client:
        response = client.get("/", params={'day': 'today'})
        assert response.status_code == 200, "Сегодня - неверный код ответа"
        assert response.json() == [
            {'id': 1, 'currency': 'USD', 'currency_value': 1.0, 'day': 'today'},
            {'id': 2, 'currency': 'EUR', 'currency_value': 1.0, 'day': 'today'}
        ], "Сегодня - неверный ответ"

        response = client.get("/", params={'day': 'yesterday'})
        assert response.status_code == 200, "Вчера - неверный код ответа"
        assert response.json() == [
            {'id': 1, 'currency': 'USD', 'currency_value': 2.0, 'day': 'yesterday'},
            {'id': 2, 'currency': 'EUR', 'currency_value': 2.0, 'day': 'yesterday'}
        ], "Вчера - неверный ответ"

        response = client.get("/", params={'day': 'before_yesterday'})
        assert response.status_code == 200, "Позавчера - неверный код ответа"
        assert response.json() == [
            {'id': 1, 'currency': 'USD', 'currency_value': 3.0, 'day': 'before_yesterday'},
            {'id': 2, 'currency': 'EUR', 'currency_value': 3.0, 'day': 'before_yesterday'}
        ], "Позавчера - неверный ответ"
