from typing import Union

from django.db import models


class RecordCreationException(Exception):
    pass


class BaseModelManager(models.Manager):
    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})

    def create(self, **kwargs):
        if "dataset" not in kwargs:
            raise RecordCreationException("You must specify a dataset for this record")

        return super().create(**kwargs)


class BaseModel(models.Model):
    YEAR_FILTER = None

    class Meta:
        abstract = True

    dataset = models.CharField(max_length=255, null=True, blank=True)

    @classmethod
    def queryset_by_year(cls, year: int, **kwargs) -> Union[models.QuerySet, list]:
        if cls.YEAR_FILTER is None:
            return []

        filters = {cls.YEAR_FILTER: year, **kwargs}
        return cls.objects.filter(**filters)

