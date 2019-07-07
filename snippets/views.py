from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework import viewsets, permissions, renderers, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib.auth.models import User

from notification.pusher import beams_client
from snippets.models import Snippet, Article, Publication
from snippets.permisssions import IsOwnerOrReadOnly
from snippets.serializers import SnippetSerializer, UserSerializer, ArticleSerializer, PublicationSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })


class SnippetFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = Snippet
        fields = ['id', 'owner', 'language', 'title', 'style']


class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewsets automatically provides `list`, `create`, `retrieve`, `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SnippetFilter
    ordering_fields = ('owner', 'title')
    ordering = ('id',)

    """
    # search and filter doesn't work together, if you have both filter will override search.
    """

    # search_fields = ('=owner__username',)

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

    @action(detail=True)
    def beams_auth(self, request, *args, **kwargs):
        # Do your normal auth checks here 🔒
        user = request.user  # get it from your auth system
        # user_id_in_query_param = request.args.get('user_id')
        if not user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        beams_token = beams_client.generate_token(user.username)
        return Response(beams_token)


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
