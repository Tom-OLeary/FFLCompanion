from rest_framework.test import APITestCase

from ffl_companion.config import App


class BaseTestCase(APITestCase):
    IMPORT_DATA = None

    @classmethod
    def setUpTestData(cls):
        App.set("testing")

        if cls.IMPORT_DATA:
            for attr, model, fixture in cls.IMPORT_DATA:
                data = bulk_create(model, fixture)
                setattr(cls, attr, data)


def bulk_create(model, rows):
    to_create = [model(**r) for r in rows]
    return model.objects.bulk_create(to_create)