from typing import Union

from django.db import models


class BaseModelManager(models.Manager):
    # def get_queryset(self):
    #     """Pre Filter for current league only"""
    #     return super().get_queryset().filter(**App.config())

    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})


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
