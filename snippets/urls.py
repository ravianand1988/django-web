from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view

from snippets.views import SnippetViewSet, UserViewSet, api_root

schema_view = get_schema_view(title='DRF Snippet API')

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'snippets', SnippetViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('schema/', schema_view),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
