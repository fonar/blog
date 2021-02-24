from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import GenericViewSet

from api.permissions import IsEditor
from article.models import Article
from .serializers import ArticleSerializer


class ArticleViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    permission_classes = [
        IsAuthenticated
    ]
    filterset_fields = {
        'status': ('exact', 'in'),
        'written_by': ('exact', ),
    }

    @action(
        methods=['patch'],
        detail=True,
        permission_classes=(IsEditor, ),
    )
    def approve(self, request, pk=None):
        article = self.get_object()
        article.status = Article.Status.APPROVED
        article.save()
        return Response(status=HTTP_200_OK)

    @action(
        methods=['patch'],
        detail=True,
        permission_classes=(IsEditor, ),
    )
    def reject(self, request, pk=None):
        article = self.get_object()
        article.status = Article.Status.REJECTED
        article.save()
        return Response(status=HTTP_200_OK)
