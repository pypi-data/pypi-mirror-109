import re
from datetime import datetime
from functions import get_normal_holidays, get_easter_week_holidays


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
