from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework import generics, views
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from permissions import *
from home.api.serializers import *
from home import models


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'posts': reverse('post-list', request=request, format=format),
    })


class UserList(generics.ListAPIView):
    """Obtains a simple list of users"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [SafeMethodsOnlyPermission]


class UserDetail(views.APIView):
    """Operations for individual users"""
    permission_classes = [SafeMethodsOnlyPermission]

    @staticmethod
    def get_user(pk):
        try:
            return User.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = UserDetail.get_user(pk)
        if request.user.is_authenticated() and request.user.pk == int(pk):
            # We're getting information about ourselves
            serializer = UserSelfSerializer(user, context={'request': request})
            return Response(serializer.data)
        else:
            # Information about another user
            serializer = UserSerializer(user, context={'request': request})
            return Response(serializer.data)


class PostList(generics.ListCreateAPIView):
    model = models.Post
    queryset = models.Post.objects.all()
    permission_classes = [AuthenticatedUserCanPostPermission]

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return PostSerializer
        else:
            return PostCreateSerializer


class PostDetail(generics.RetrieveAPIView):
    model = models.Post
    queryset = models.Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [SafeMethodsOnlyPermission]


class PostImage(generics.RetrieveAPIView):
    model = models.Post
    queryset = models.Post.objects.all()
    serializer_class = PostImageSerializer
    permission_classes = [UserCanOnlyViewPostOncePermission]
