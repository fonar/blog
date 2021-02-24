from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory
from factory import Faker


class UserFactory(DjangoModelFactory):
    email = Faker('email')
    username = Faker('user_name')

    class Meta:
        model = get_user_model()
