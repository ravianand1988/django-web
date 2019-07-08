from rest_framework import serializers
from django.contrib.auth.models import User, Group

from .models import Snippet, Article, Publication


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        fields = ('url', 'id', 'highlight', 'owner', 'title', 'code', 'linenos', 'language', 'style')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'snippets')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name', )


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    reset = serializers.HyperlinkedIdentityField(view_name='article-reset')
    publications = serializers.HyperlinkedRelatedField(many=True, view_name='publication-detail', read_only=True)

    class Meta:
        model = Article
        fields = ('url', 'id', 'headline', 'publications', 'reset')


class PublicationSerializer(serializers.HyperlinkedRelatedField):
    class Meta:
        model = Publication
        fields = ['id', 'title']
