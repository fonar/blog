from rest_framework.routers import DefaultRouter

from api.article.views import ArticleViewSet
from api.writer.views import WriterViewSet


app_name = 'api'
router = DefaultRouter()

router.register(r'article', ArticleViewSet, basename='article')
router.register(r'writer', WriterViewSet, basename='writer')

urlpatterns = router.urls
