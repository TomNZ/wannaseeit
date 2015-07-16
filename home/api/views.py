from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework import generics, views, pagination, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from permissions import *
from renderers import *
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
    # By default this view should never be used - enabling it for admins only to make development easier
    permission_classes = [permissions.IsAdminUser]


class UserDetail(views.APIView):
    """Operations for individual users"""
    permission_classes = [SafeMethodsOnlyPermission]

    @staticmethod
    def get_user(pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
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
    pagination_class = pagination.CursorPagination
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('when_posted',)
    ordering = ('-when_posted',)

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return PostSerializer
        else:
            return PostCreateSerializer

    def perform_create(self, serializer):
        # On create, set the current user as the owner of the post
        serializer.save(user=self.request.user)


class PostDetail(generics.RetrieveAPIView):
    model = models.Post
    queryset = models.Post.objects.all()
    permission_classes = [SafeMethodsOnlyPermission]

    def get_serializer_class(self):
        return PostSerializer


class PostImage(generics.RetrieveAPIView):
    model = models.Post
    queryset = models.Post.objects.all()
    serializer_class = PostImageSerializer
    permission_classes = [UserCanOnlyViewPostOncePermission]
    renderer_classes = (ImageRenderer,)
