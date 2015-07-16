from django.contrib.auth.models import User
from home import models
from rest_framework import serializers


class UserSelfSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for use when grabbing information about the current user"""

    class Meta:
        model = User
        fields = ('url', 'username', 'email',)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer to grab limited information about other users"""

    class Meta:
        model = User
        fields = ('url', 'username',)


class PostSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for viewing posts"""
    user = UserSerializer(read_only=True)
    # Include a special hyperlink to request the post's image
    image = serializers.HyperlinkedIdentityField(source='pk', view_name='post-image')

    class Meta:
        model = models.Post
        fields = ('url', 'user', 'when_posted', 'caption', 'image',)


class PostCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating posts only"""

    class Meta:
        model = models.Post
        fields = ('caption', 'image',)


# TODO: Change into ModelSerializer, and hook up the image field
class PostImageSerializer(serializers.Serializer):
    """Serializer for outputting just the image details"""

    image = serializers.CharField(max_length=None, default='test.jpg')

    class Meta:
        fields = ('image',)
