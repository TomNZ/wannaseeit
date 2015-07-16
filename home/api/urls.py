from django.conf.urls import patterns, include, url
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from home.api.views import *

default_router = routers.DefaultRouter()

user_urls = [
    url(r'^/(?P<pk>[0-9]+)/?$',
        UserDetail.as_view(),
        name='user-detail'),

    url(r'^/register/?$',
        UserCreate.as_view(),
        name='user-create'),

    url(r'^/?$',
        UserList.as_view(),
        name='user-list'),
]

post_urls = [
    url(r'^/unseen/?$',
        UnseenPostList.as_view(),
        name='post-unseen'),

    url(r'^/(?P<pk>[0-9]+)/?$',
        PostDetail.as_view(),
        name='post-detail'),

    url(r'^/(?P<pk>[0-9]+)/image/?$',
        PostImage.as_view(),
        name='post-image'),

    url(r'^/?$',
        PostList.as_view(),
        name='post-list'),
]

urlpatterns = [
    # Include a root page for API discovery
    url(r'^$', wanna_see_it, name='wanna-see-it'),

    # User URLs
    url(r'^users', include(user_urls)),

    # Post URLs
    url(r'^posts', include(post_urls)),
]

urlpatterns = format_suffix_patterns(urlpatterns)
