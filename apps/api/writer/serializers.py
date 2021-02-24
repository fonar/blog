from rest_framework.serializers import IntegerField, ModelSerializer

from writer.models import Writer


class WriterSerializer(ModelSerializer):
    articles_count = IntegerField()
    articles_last_30_count = IntegerField()

    class Meta:
        model = Writer

        fields = (
            'pk',
            'name',
            'articles_count',
            'articles_last_30_count',
        )
