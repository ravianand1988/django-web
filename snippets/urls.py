from django.urls import path, include
from rest_framework.routers import DefaultRouter

from snippets.views import SnippetViewSet, UserViewSet, api_root

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'snippets', SnippetViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
