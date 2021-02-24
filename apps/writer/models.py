from django.contrib.auth import get_user_model
from django.db.models import BooleanField, CASCADE, CharField, Model, OneToOneField


class Writer(Model):
    name = CharField(max_length=255)
    is_editor = BooleanField()

    user = OneToOneField(
        get_user_model(),
        on_delete=CASCADE,
        related_name='writer',
    )
