from datetime import timedelta

from django.utils import timezone
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK

from article.models import Article


def test_writer_list_200(anonymous_client, articles, django_assert_max_num_queries):

    with django_assert_max_num_queries(1):
        response = anonymous_client.get(
            reverse('api:writer-list'),
        )
    assert response.status_code == HTTP_200_OK

    for writer in response.data:
        assert writer['articles_count'] == Article.objects.filter(
            written_by=writer['pk']
        ).count()

        assert writer['articles_last_30_count'] == Article.objects.filter(
            written_by=writer['pk']
        ).filter(
            created_at__gt=(timezone.now() - timedelta(days=30))
        ).count()
