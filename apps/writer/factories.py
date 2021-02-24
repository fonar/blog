from factory.django import DjangoModelFactory
from factory import Faker, SubFactory

from writer.models import Writer


class WriterFactory(DjangoModelFactory):
    name = Faker('name')
    is_editor = Faker('boolean')

    user = SubFactory(
        'user.factories.UserFactory',
    )

    class Meta:
        model = Writer
