from django.db.models import CharField, DateTimeField, ForeignKey, Model, PROTECT, TextChoices, TextField
from django.utils.translation import gettext_lazy as _


class Article(Model):
    class Status(TextChoices):
        NEW = 'new', _('New')
        APPROVED = 'approved', _('Approved')
        REJECTED = 'rejected', _('Rejeced')

    title = CharField(max_length=255)
    content = TextField()

    status = TextField(
        max_length=16,
        choices=Status.choices,
        default=Status.NEW,
        db_index=True,
    )
    created_at = DateTimeField(auto_now_add=True)
    written_by = ForeignKey(
        'writer.Writer',
        related_name='written_articles',
        on_delete=PROTECT,
    )
    edited_by = ForeignKey(
        'writer.Writer',
        related_name='edited_articles',
        on_delete=PROTECT,
    )
