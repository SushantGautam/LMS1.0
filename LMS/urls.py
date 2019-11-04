from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from  WebApp import views
from django.contrib.auth.decorators import login_required, user_passes_test

from decorator_include import decorator_include
from LMS.decorators import authorize

from rest_framework import routers

from WebApp import api

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^quiz/', include('quiz.urls')),
    # path('', include('WebApp.urls')),
    # path('', decorator_include([login_required, authorize(lambda u: u.Is_CenterAdmin)], 'WebApp.urls')),
    # path('students/',decorator_include([login_required, authorize(lambda u: u.Is_Student)], 'WebApp.student_module.urls')),
    # path('teachers/',decorator_include([login_required, authorize(lambda u: u.Is_Teacher)], 'WebApp.teacher_module.urls')),
    path('', decorator_include(login_required, 'WebApp.urls')),
    path('students/',decorator_include(login_required, 'WebApp.student_module.urls')),
    path('teachers/',decorator_include(login_required, 'WebApp.teacher_module.urls')),

    url(r'^$', views.start, name='start'),
    path('forum/',include('forum.urls')),
    path('survey/',include('survey.urls')),
    url(r'^login/$', views.login, {'template_name': 'registration/login.html',
                                   'redirect_authenticated_user': True}, name='login'),

    url(r'^.*logout/$', views.logout,
        {'template_name': 'registration/logout.html', 'next_page': '/'}, name='logout'),

#     url(r'^.*editprofile/$', views.editprofile, name='editprofile'),

    url(r'^successlogin/$', views.loginsuccess, name='loginsuccess'),

    url(r'^.*register/$', views.register.as_view(), name='register'),
    path('ajax/validate_username/', views.validate_username, name='validate_username'),
    path('ajax/validate_password/', views.validate_password, name='validate_password'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

router = routers.DefaultRouter()

router.register(r'centerinfo', api.CenterInfoViewSet)
router.register(r'memberinfo', api.MemberInfoViewSet)
router.register(r'courseinfo', api.CourseInfoViewSet)
router.register(r'chapterinfo', api.ChapterInfoViewSet)
router.register(r'inninginfo', api.InningInfoViewSet)
router.register(r'sessioninfo', api.SessionInfoViewSet)
router.register(r'assignassignmentinfo', api.AssignAssignmentInfoViewSet)
router.register(r'inninggroup', api.InningGroupViewSet)
router.register(r'groupmapping', api.GroupMappingViewSet)
router.register(r'assignmentinfo', api.AssignmentInfoViewSet)
router.register(r'assignanswerinfo', api.AssignAnswerInfoViewSet)
router.register(r'questioninfo', api.QuestionInfoViewSet)

urlpatterns += [
    # urls for Django Rest Framework API
    path('api/v1/', include(router.urls)),
    path('api/v1/chaptercontent/<int:chapterID>', api.ChapterContent.as_view(), name='chaptercontent'),
]

urlpatterns += [
    # urls for chapterpagebuilder
    path('3DViewer/<path:urlpath>',
         views.ThreeDViewer, name='3DViewer'),
    path('3DViewer/',
         views.ThreeDViewer, name='3DViewer'),
]