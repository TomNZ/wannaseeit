from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from rest_framework import generics, views, pagination, filters, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from permissions import *
from home.api.serializers import *
from home import models
from PIL import Image


@api_view(('GET',))
def wanna_see_it(request, format=None):
    """Register a new user, or view a list of posts"""
    return Response({
        'register': reverse('user-create', request=request, format=format),
        'posts': reverse('post-list', request=request, format=format),
        'users': reverse('user-list', request=request, format=format),
    })


class UserList(generics.ListAPIView):
    """Retrieve a list of users"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # By default this view should never be used - enabling it for admins only to make development easier
    permission_classes = [permissions.IsAdminUser]


class UserCreate(generics.CreateAPIView):
    """Register a new user"""
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    # Only non-logged-in users should be able to register
    permission_classes = [NotAuthenticatedPermission]


class UserDetail(views.APIView):
    """Retrieve information about a given user - returns additional information if this user is ourself"""
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
    """List all recent posts, and create new posts"""
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
    """View details about a given post"""
    model = models.Post
    queryset = models.Post.objects.all()
    permission_classes = [SafeMethodsOnlyPermission]

    def get_serializer_class(self):
        return PostSerializer


class PostImage(views.APIView):
    """View the image associated with a given post, if allowed"""
    model = models.Post
    queryset = models.Post.objects.all()
    serializer_class = PostImageSerializer
    permission_classes = [UserCanOnlyViewPostOncePermission]

    def get(self, request, pk, format=None):
        # First, grab the post
        post = get_object_or_404(models.Post, pk=pk)

        if request.user.is_authenticated() and not post.viewed_by(request.user):
            # We're actually allowed to view!
            # We use PIL to ensure that the output is JPEG no matter the input
            img = Image.open(post.image.file)
            response = HttpResponse(content_type='image/jpeg')
            img.save(response, "JPEG")

            # Set the viewed flag for this user
            view = models.UserViewedPost(user=request.user, post=post)
            view.save()

            # Send the response
            return response
        else:
            # Invalid request
            return Response(status=status.HTTP_403_FORBIDDEN)
