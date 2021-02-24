import random

import factory
import pytest
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_403_FORBIDDEN

from article.factories import ArticleFactory
from article.models import Article
from writer.models import Writer


@pytest.fixture
def article_data():
    yield factory.build(dict, FACTORY_CLASS=ArticleFactory)


def test_article_create_201(writer, writer_client, article_data):
    response = writer_client.post(reverse('api:article-list'), article_data)
    assert response.status_code == HTTP_201_CREATED

    assert response.data.get('written_by') == writer.user.pk
    assert response.data.get('edited_by') == writer.user.pk
    assert response.data.get('status') == Article.Status.NEW

    for field in ('written_by', 'edited_by', 'status', 'created_at'):
        del article_data[field]

    assert response.data.items() >= article_data.items()


def test_article_create_403(anonymous_client, article_data):
    response = anonymous_client.post(reverse('api:article-list'), article_data)
    assert response.status_code == HTTP_403_FORBIDDEN


def test_article_update_200(writer, writer_client, article_data, article):
    response = writer_client.patch(reverse('api:article-detail', args=(article.pk, )), article_data)
    assert response.status_code == HTTP_200_OK

    assert response.data.get('edited_by') == writer.user.pk

    for field in ('written_by', 'edited_by', 'status', 'created_at'):
        del article_data[field]

    assert response.data.items() >= article_data.items()


def test_article_update_403(anonymous_client, writer, article, article_data):
    response = anonymous_client.patch(reverse('api:article-detail', args=(article.pk, )), article_data)
    assert response.status_code == HTTP_403_FORBIDDEN


def test_article_list_200(writer_client, articles, django_assert_max_num_queries):

    statuses = random.sample(
        Article.Status.values,
        random.randrange(
            0,
            len(Article.Status.values)
        )
    )
    writer = Writer.objects.order_by("?").first()

    with django_assert_max_num_queries(2):
        response = writer_client.get(
            reverse('api:article-list'),
            {
                'written_by': writer.pk,
                'status__in': ','.join(statuses)
            },
        )
    assert response.status_code == HTTP_200_OK

    for article in response.data:
        assert article['status'] in statuses
        assert article['written_by'] == writer.pk


def test_article_approve_200(editor, editor_client, article):

    response = editor_client.patch(
        reverse(
            'api:article-approve',
            args=(article.pk, ),
        ),
    )
    article.refresh_from_db()

    assert response.status_code == HTTP_200_OK
    assert article.status == Article.Status.APPROVED


def test_article_approve_403(editor, not_editor_client, article):

    response = not_editor_client.patch(
        reverse(
            'api:article-approve',
            args=(article.pk, ),
        ),
    )
    assert response.status_code == HTTP_403_FORBIDDEN


def test_article_reject_200(editor, editor_client, article):

    response = editor_client.patch(
        reverse(
            'api:article-reject',
            args=(article.pk, ),
        ),
    )
    article.refresh_from_db()

    assert response.status_code == HTTP_200_OK
    assert article.status == Article.Status.REJECTED


def test_article_reject_403(editor, not_editor_client, article):

    response = not_editor_client.patch(
        reverse(
            'api:article-reject',
            args=(article.pk, ),
        ),
    )
    assert response.status_code == HTTP_403_FORBIDDEN
