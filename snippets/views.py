from rest_framework import viewsets, permissions, renderers, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib.auth.models import User

from snippets.models import Snippet, Article, Publication
from snippets.permisssions import IsOwnerOrReadOnly
from snippets.serializers import SnippetSerializer, UserSerializer, ArticleSerializer, PublicationSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })


class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewsets automatically provides `list`, `create`, `retrieve`, `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """

    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """This viewset automatically provide `list` and `detail` actions."""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    """
    This viewsets automatically provides `list`, `create`, `retrieve`, `update` and `destroy` actions.

    Additionally we also provide an extra `reset` action.
    """

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    @action(detail=True)
    def reset(self, request, *args, **kwargs):
        article = self.get_object()
        article.reset()
        serializer = self.get_serializer(article)
        return Response(serializer.data)


class PublicationViewSet(viewsets.ModelViewSet):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
