from home import models
from rest_framework import permissions


class NotAuthenticatedPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_authenticated()


class SafeMethodsOnlyPermission(permissions.BasePermission):
    """Only can access non-destructive methods (like GET and HEAD)"""

    def has_permission(self, request, view):
        return self.has_object_permission(request, view)

    def has_object_permission(self, request, view, obj=None):
        return request.method in permissions.SAFE_METHODS


class AuthenticatedUserCanPostPermission(SafeMethodsOnlyPermission):
    """Allow anyone to view, but only registered users can create"""

    def has_object_permission(self, request, view, obj=None):
        if request.method in permissions.SAFE_METHODS:
            # This is a read - allow
            return True
        else:
            if obj:
                # Object has been passed, so this is an update
                # TODO: Allow updates to posts - for now we just deny the request
                return False
            else:
                # This is a new object write - user must be authenticated
                return request.user.is_authenticated()


class UserCanOnlyViewPostOncePermission(SafeMethodsOnlyPermission):
    """Allow users to view a post only once - and deny non-authenticated users"""

    def has_object_permission(self, request, view, obj=None):
        if request.method in permissions.SAFE_METHODS:
            if request.user.is_authenticated():
                # See if the user has seen this item
                # TODO: Set this row when rendering the actual view
                viewed = models.UserViewedPost.objects.filter(user=request.user, post=obj).exists()
                return not viewed
            else:
                # Anonymous user - deny viewing
                return False
        else:
            # Deny any write/update requests
            return False
