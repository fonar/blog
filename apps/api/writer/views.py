from datetime import timedelta
from django.db.models import Count, Q
from django.utils import timezone

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin

from writer.models import Writer
from .serializers import WriterSerializer


class WriterViewSet(
    ListModelMixin,
    GenericViewSet,
):
    serializer_class = WriterSerializer

    def get_queryset(self):
        return Writer.objects.all().annotate(
            articles_count=Count(
                'written_articles',
            ),
        ).annotate(
            articles_last_30_count=Count(
                'written_articles',
                filter=Q(
                    written_articles__created_at__gt=(
                        timezone.now() - timedelta(days=30)
                    ),
                ),
            ),
        )
