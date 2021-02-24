import pytz
from factory import Faker, post_generation
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice

from article.models import Article
from writer.models import Writer


class ArticleFactory(DjangoModelFactory):
    title = Faker('pystr', max_chars=255)
    content = Faker('text')

    created_at = Faker(
        'date_time_between',
        start_date='-1y',
        end_date='now',
        tzinfo=pytz.utc,
    )
    status = FuzzyChoice(
        Article.Status.values,
    )
    written_by = FuzzyChoice(
        Writer.objects.all(),
    )
    edited_by = FuzzyChoice(
        Writer.objects.all(),
    )
    edited_by = FuzzyChoice(
        Writer.objects.all(),
    )

    @post_generation
    def created_at_post_save(obj, create, extracted, **kwargs):
        """
        Set created_at again as first time its rewrited in .save()
        """
        if type(obj) is not dict:
            if create:
                params = dict(ArticleFactory.created_at._defaults)
                params.update({'locale': 'en-us'})
                obj.created_at = ArticleFactory.created_at.evaluate(
                    None, None, params,
                )
                obj.save()

    class Meta:
        model = Article
