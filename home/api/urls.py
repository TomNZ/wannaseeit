from django.conf.urls import patterns, include, url
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from home.api.views import *

default_router = routers.DefaultRouter()

urlpatterns = [
    # Include a root page for API discovery
    url(r'^$', api_root, name='api-root'),

    url(r'^users/?$',
        UserList.as_view(),
        name='user-list'),

    url(r'^users/(?P<pk>[0-9]+)/?$',
        UserDetail.as_view(),
        name='user-detail'),

    url(r'^posts/?$',
        PostList.as_view(),
        name='post-list'),

    url(r'^posts/(?P<pk>[0-9]+)/?$',
        PostDetail.as_view(),
        name='post-detail'),

    url(r'^posts/(?P<pk>[0-9]+)/image/?$',
        PostImage.as_view(),
        name='post-image'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
