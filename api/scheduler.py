import operations
from rocketry import Rocketry

roc = Rocketry()


@roc.task('every 10 seconds')
def get_daily_rate():
    rates = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    usd = rates['Valute']['USD']
    eur = rates['Valute']['EUR']


if __name__ == "__main__":
    roc.run()
