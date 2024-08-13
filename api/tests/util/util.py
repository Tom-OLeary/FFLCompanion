from rest_framework.test import APITestCase

from owner.models import Owner


class BaseTestCase(APITestCase):
    IMPORT_DATA = None

    @classmethod
    def setUpTestData(cls):
        cls.user = Owner.objects.create_owner(
            name="User1",
            username="test.owner",
            password="password",
            dataset="testing",
        )

        if cls.IMPORT_DATA:
            for attr, model, fixture in cls.IMPORT_DATA:
                data = bulk_create(model, fixture)
                setattr(cls, attr, data)

    def setUp(self):
        self.client.force_authenticate(self.user)
        self.generate_data()

    def generate_data(self):
        return


def bulk_create(model, rows):
    to_create = [model(**r) for r in rows]
    return model.objects.bulk_create(to_create)
