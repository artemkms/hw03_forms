import datetime

today = datetime.date.today()
today_year = int(today.year)


def year(request):
    """Добавляет переменную с текущим годом."""
    return {
        'year': today_year,
    }
