import pytest
from rest_framework.test import APIClient

from article.factories import ArticleFactory
from writer.factories import WriterFactory


@pytest.fixture
def writers():
    yield WriterFactory.create_batch(10)


@pytest.fixture
def articles(writers):
    yield ArticleFactory.create_batch(1000)


@pytest.fixture()
def writer():
    yield WriterFactory()


@pytest.fixture()
def article():
    yield ArticleFactory()


@pytest.fixture()
def editor():
    yield WriterFactory(is_editor=True)


@pytest.fixture()
def not_editor():
    yield WriterFactory(is_editor=False)


@pytest.fixture()
def writer_client(writer):
    client = APIClient()
    client.force_authenticate(writer.user)
    return client


@pytest.fixture()
def editor_client(editor):
    client = APIClient()
    client.force_authenticate(editor.user)
    return client


@pytest.fixture()
def not_editor_client(not_editor):
    client = APIClient()
    client.force_authenticate(not_editor.user)
    return client


@pytest.fixture()
def anonymous_client():
    yield APIClient()


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    ...
