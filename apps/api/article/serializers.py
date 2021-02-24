from django.utils.functional import cached_property
from rest_framework.serializers import ModelSerializer

from article.models import Article


class ArticleSerializer(ModelSerializer):

    class Meta:
        model = Article

        fields = (
            'title',
            'content',

            'pk',
            'status',
            'created_at',
            'written_by',
            'edited_by',
        )
        read_only_fields = (
            'id',
            'status',
            'created_at',
            'written_by',
            'edited_by',
        )

    @cached_property
    def writer(self):
        return self.context['request'].user.writer

    def create(self, validated_data):
        validated_data.update({
            'written_by': self.writer,
            'edited_by': self.writer,
        })
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.update({
            'edited_by': self.writer,
        })
        return super().update(instance, validated_data)
