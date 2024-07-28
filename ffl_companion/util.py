from datetime import date, datetime
from typing import Union


def format_date_str(day: str) -> Union[date, str]:
    if "/" in day:
        return datetime.strptime(day, "%m/%d/%y").date()
    return day

