from datetime import date, datetime
from typing import Union

from django.db.models import QuerySet, Model, Manager


class BaseModelManager(Manager):
    pass


class BaseModel(Model):
    YEAR_FILTER = None

    class Meta:
        abstract = True

    @classmethod
    def queryset_by_year(cls, year: int, **kwargs) -> QuerySet:
        filters = {cls.YEAR_FILTER: year, **kwargs}
        return cls.objects.filter(**filters)


def format_date_str(day: str) -> Union[date, str]:
    if "/" in day:
        return datetime.strptime(day, "%m/%d/%y").date()
    return day

