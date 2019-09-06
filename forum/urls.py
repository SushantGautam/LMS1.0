# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from django.urls import path
from . import api
from . import views

app_name = "forum"
api_router = routers.DefaultRouter()
router = routers.DefaultRouter()
router.register(r'thread', api.ThreadViewSet)
router.register(r'post', api.PostViewSet)
router.register(r'notification', api.NotificationViewSet)
router.register(r'nodegroup', api.NodeGroupViewSet)
router.register(r'topic', api.TopicViewSet)

urlpatterns = [
    path(r'^page/(?P<page>[0-9]+)/$', views.Index.as_view(), name='index'),
    path(r'', views.Index.as_view(), name='index'),
    path(r'^topic/(?P<pk>\d+)/page/(?P<page>[0-9]+)/$',
         views.TopicView.as_view(), name='topic'),
    path('topic/<int:pk>/', views.TopicView.as_view(), name='topic'),
    path(r'^nodegroup/(?P<pk>\d+)/page/(?P<page>[0-9]+)/$',
         views.NodeGroupView.as_view(), name='nodegroup'),
    path('nodegroup/<int:pk>/', views.NodeGroupView.as_view(), name='nodegroup'),
    path(r't/edit/<int:pk>/', views.edit_thread, name='edit_thread'),
    path(r'post/edit/<int:pk>/', views.edit_post, name='edit_post'),
    path(r'topic/edit/<int:pk>/', views.edit_topic, name='edit_topic'),
    path(r't/append/<int:pk>/', views.create_appendix, name='create_appendix'),
    path(r'^t/(?P<pk>\d+)/page/(?P<page>[0-9]+)/$',
         views.ThreadView.as_view(), name='thread'),
    path(r't/<int:pk>/', views.ThreadView.as_view(), name='thread'),
    path(r'u/<int:pk>/', views.user_info, name='user_info'),
    path(r'^u/(?P<pk>\d+)/threads/page/(?P<page>[0-9]+)/$',
         views.UserThreads.as_view(), name='user_threads'),
    path(r'u/threads/<int:pk>/', views.UserThreads.as_view(), name='user_threads'),
    path(r'^u/(?P<pk>\d+)/posts/page/(?P<page>[0-9]+)/$',
         views.UserPosts.as_view(), name='user_posts'),
    path(r'u/posts/<int:pk>/', views.UserPosts.as_view(), name='user_posts'),
    path(r'login/', views.login_view, name='login'),
    path(r'reg/', views.reg_view, name='reg'),
    path(r'logout/', views.logout_view, name="logout"),
    path(r'search/', views.search_redirect, name='search_redirect'),
    path(r'^search/(?P<keyword>.*?)/page/(?P<page>[0-9]+)/$',
         views.SearchView.as_view(), name='search'),
    path(r'search/(?P<keyword>.*)/', views.SearchView.as_view(), name='search'),
    path(r't/create/', views.create_thread, name='create_thread'),
    path(r't/create/(?P<nodegroup_pk>\d+)/',
         views.create_thread, name='create_thread'),
    path(r't/create/(?P<nodegroup_pk>\d+)/(?P<topic_pk>\d+)/',
         views.create_thread, name='create_thread'),
    path(r'topic/create/', views.create_topic, name='create_topic'),
    path(r'topic/create/(?P<nodegroup_pk>\d+)',
         views.create_topic, name='create_topic'),
    path(r'notifications/', views.NotificationView.as_view(), name='notifications'),
    path(r'avatar/', views.upload_avatar, name="upload_avatar"),
    path(r'api/v1/', include(router.urls)),
]
