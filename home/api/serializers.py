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
    viewed = serializers.SerializerMethodField('post_viewed')

    class Meta:
        model = models.Post
        fields = ('url', 'user', 'when_posted', 'caption', 'viewed', 'image',)

    def post_viewed(self, obj):
        if self.context['request'].user.is_authenticated():
            return obj.viewed_by(self.context['request'].user)
        else:
            return False


class PostCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating posts only - limit what can be modified"""
    # Read-only fields for display of the created object
    url = serializers.HyperlinkedIdentityField(source='pk', view_name='post-detail', read_only=True)
    user = UserSerializer(read_only=True)
    when_posted = serializers.DateTimeField(read_only=True)
    image = serializers.HyperlinkedIdentityField(source='pk', view_name='post-image', read_only=True)

    # Special write-only field for doing the image upload
    image_upload = serializers.ImageField(source='image', write_only=True)

    class Meta:
        model = models.Post
        fields = ('url', 'user', 'when_posted', 'caption', 'image', 'image_upload',)


# TODO: Change into ModelSerializer, and hook up the image field
class PostImageSerializer(serializers.Serializer):
    """Serializer for outputting just the image details"""

    image = serializers.CharField(max_length=None, default='test.jpg')

    class Meta:
        fields = ('image',)
