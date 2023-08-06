from datetime import timedelta, datetime
from constants import HOLIDAYS, EASTER_WEEK_HOLIDAYS

"""Easter is observed by the churches of the West on the first Sunday 
following the full moon that occurs on or following the spring equinox (
March 21). Easter is a "movable" feast which can occur as early as March 22 
or as late as April 25. """


def butcher_algorithm(year):
    a = year % 19
    b = year // 100
    c = year % 100
    d = (19 * a + b - b // 4 - ((b - (b + 8) // 25 + 1) // 3) + 15) % 30
    e = (32 + 2 * (b % 4) + 2 * (c // 4) - d - (c % 4)) % 7
    f = d + e - 7 * ((a + 11 * d + 22 * e) // 451) + 114
    month = f // 31
    day = f % 31 + 1
    return datetime(year, month, day)


def next_day(day, days_to_sum):
    new_date = day if days_to_sum == 7 else day + timedelta(
        days=(0 - day.weekday()) % 7)
    return str(new_date.date())


def get_normal_holidays(year: int):
    normal_holidays = []
    for i in HOLIDAYS:
        normal_holidays.append({
            "holiday": next_day(
                datetime.strptime(f"{year}-{i.get('day')}", "%Y-%m-%d"),
                int(i.get('daysToSum'))),
            "celebrationDay": str(datetime.strptime(f"{year}-{i.get('day')}",
                                                    "%Y-%m-%d").date()),
            "celebration": i.get('celebration')

        })
    return normal_holidays


def get_easter_week_holidays(year: int):
    sunday = butcher_algorithm(year).date()
    easter_week_holidays = []
    for i in EASTER_WEEK_HOLIDAYS:
        day = sunday + timedelta(days=i.get('day'))
        easter_week_holidays.append({
            "holiday": str(day),
            "celebrationDay": str(day),
            "celebration": i.get('celebration')
        })
    return easter_week_holidays
