from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view

from snippets.views import SnippetViewSet, UserViewSet, ArticleViewSet, PublicationViewSet, GroupViewSet

schema_view = get_schema_view(title='DRF Snippet API')

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'snippets', SnippetViewSet, base_name='snippet')
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'articles', ArticleViewSet)
router.register(r'publications', PublicationViewSet)
urlpatterns = [
    path('schema/', schema_view),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('auth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
