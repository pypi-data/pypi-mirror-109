# colombiaHolidays

## Description
Based on [nequibc /colombia-holidays](https://github.com/nequibc/colombia-holidays) and adapted to use as a python 
module to return the list of holidays existing on a determined year in Colombia.

It also returns a boolean that indicates if today is a holiday.

## Installation
```shell
pip install colombiaHolidays
```

## How to use

You can import the package and call each one of the following methods 
depending on your need.

### holidays_by_year
Returns a list of holidays existing on a determined year in Colombia 
between 1970 and 99999, and each holiday has the following structure:

```shell
{
    'holiday': '2021-01-01', 
    'celebrationDay': '2021-01-01', 
    'celebration': 'Año Nuevo'
}
```

### is_today_holiday
Returns a boolean (True or False) that indicates whether is this day a 
holiday or not.

## Contact
Oscar Cely - oscarcej@gmail.com