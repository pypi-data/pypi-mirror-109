import re
from datetime import datetime, timedelta

# Constants

NEXT_DAY = {
    "SUNDAY": 0,
    "MONDAY": 1,
    "TUESDAY": 2,
    "WEDNESDAY": 3,
    "THURSDAY": 4,
    "FRIDAY": 5,
    "SATURDAY": 6,
    "NONE": 7
}

EASTER_WEEK_HOLIDAYS = [
    {
        "day": -3,
        "daysToSum": NEXT_DAY['NONE'],
        "celebration": 'Jueves Santo'
    },
    {
        "day": -2,
        "daysToSum": NEXT_DAY['NONE'],
        "celebration": 'Viernes Santo'
    },
    {
        "day": 43,
        "daysToSum": NEXT_DAY["MONDAY"],
        "celebration": 'Ascensión del Señor'
    },
    {
        "day": 64,
        "daysToSum": NEXT_DAY["MONDAY"],
        "celebration": 'Corphus Christi'
    },
    {
        "day": 71,
        "daysToSum": NEXT_DAY["MONDAY"],
        "celebration": 'Sagrado Corazón de Jesús'
    }
]

HOLIDAYS = [
    {
        "day": '01-01',
        "daysToSum": NEXT_DAY["NONE"],
        "celebration": 'Año Nuevo'
    },
    {
        "day": '05-01',
        "daysToSum": NEXT_DAY["NONE"],
        "celebration": 'Día del Trabajo'
    },
    {
        "day": '07-20',
        "daysToSum": NEXT_DAY["NONE"],
        "celebration": 'Día de la Independencia'
    },
    {
        "day": '08-07',
        "daysToSum": NEXT_DAY["NONE"],
        "celebration": 'Batalla de Boyacá'
    },
    {
        "day": '12-08',
        "daysToSum": NEXT_DAY["NONE"],
        "celebration": 'Día de la Inmaculada Concepción'
    },
    {
        "day": '12-25',
        "daysToSum": NEXT_DAY["NONE"],
        "celebration": 'Día de Navidad'
    },
    {
        "day": '01-06',
        "daysToSum": NEXT_DAY["MONDAY"],
        "celebration": 'Día de los Reyes Magos'
    },
    {
        "day": '03-19',
        "daysToSum": NEXT_DAY["MONDAY"],
        "celebration": 'Día de San José'
    },
    {
        "day": '06-29',
        "daysToSum": NEXT_DAY["MONDAY"],
        "celebration": 'San Pedro y San Pablo'
    },
    {
        "day": '08-15',
        "daysToSum": NEXT_DAY["MONDAY"],
        "celebration": 'La Asunción de la Virgen'
    },
    {
        "day": '10-12',
        "daysToSum": NEXT_DAY["MONDAY"],
        "celebration": 'Día de la Raza'
    },
    {
        "day": '11-01',
        "daysToSum": NEXT_DAY["MONDAY"],
        "celebration": 'Todos los Santos'
    },
    {
        "day": '11-11',
        "daysToSum": NEXT_DAY["MONDAY"],
        "celebration": 'Independencia de Cartagena'
    }
]

# Functions


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


# Main functions

def holidays_by_year(year: int) -> list:
    if year is None:
        raise ValueError("No year provided")
    if not bool(re.match("^\d*$", str(year))):
        raise ValueError("The year must be an integer")
    if year < 1970 or year > 99999:
        raise ValueError('The year should be greater to 1969 and smaller to '
                         '100000')
    return sorted(get_normal_holidays(year) + get_easter_week_holidays(year),
                  key=lambda x: datetime.strptime(x.get('holiday'),
                                                  '%Y-%m-%d'))


def is_today_holiday() -> bool:
    return str(datetime.now().date()) in [x.get('holiday') for x in
                                          holidays_by_year(
                                              datetime.now().year)]
