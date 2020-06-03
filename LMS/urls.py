from decorator_include import decorator_include
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path
from rest_framework import routers

from WebApp import api
from WebApp import views
from WebApp.student_module.views import loginforapp, singleUserHomePageJSON, studentCourseProgress

urlpatterns = [
                  url(r'^admin/', admin.site.urls),
                  url(r'^rest-auth/', include('rest_auth.urls')),
                  url(r'^quiz/', include('quiz.urls')),
                  # path('', include('WebApp.urls')),
                  # path('', decorator_include([login_required, authorize(lambda u: u.Is_CenterAdmin)], 'WebApp.urls')),
                  # path('students/',decorator_include([login_required, authorize(lambda u: u.Is_Student)], 'WebApp.student_module.urls')),
                  # path('teachers/',decorator_include([login_required, authorize(lambda u: u.Is_Teacher)], 'WebApp.teacher_module.urls')),
                  path('', decorator_include(login_required, 'WebApp.urls')),
                  path('students/', decorator_include(login_required, 'WebApp.student_module.urls')),
                  path('teachers/', decorator_include(login_required, 'WebApp.teacher_module.urls')),
                  path('courseinfo/<int:course>/chapterinfo/<int:chapter>/offline_contents',
                       views.OfflineContentsView.as_view(), name='offlinecontentviewer'),
                  url(r'^$', views.start, name='start'),
                  path('forum/', include('forum.urls')),
                  path('survey/', include('survey.urls')),
                  url(r'^login/$', views.login, {'template_name': 'registration/login.html',
                                                 'redirect_authenticated_user': True}, name='login'),
                  path(
                      'students/courseinfo/<int:course>/chapterinfo/<int:chapter>/contentforapp/<slug:username>/<slug:password>/',
                      loginforapp, name='loginforapp'),

                  url(r'^.*logout/$', views.logout,
                      {'template_name': 'registration/logout.html', 'next_page': '/'}, name='logout'),

                  #     url(r'^.*editprofile/$', views.editprofile, name='editprofile'),

                  url(r'^successlogin/$', views.loginsuccess, name='loginsuccess'),

                  url(r'^.*register/$', views.register.as_view(), name='register'),
                  path('ajax/validate_username/', views.validate_username, name='validate_username'),
                  path('ajax/validate_password/', views.validate_password, name='validate_password'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                         document_root=settings.STATIC_ROOT)

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
router.register(r'attendance', api.AttendanceViewSet)

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

    path('summernote/', include('django_summernote.urls')),
]

urlpatterns += [
    # urls for chapterpagebuilder
    path('gitpull', views.gitpull),
]
handler400 = 'WebApp.views.error_400'
handler403 = 'WebApp.views.error_403'
handler404 = 'WebApp.views.error_404'
handler500 = 'WebApp.views.error_500'

urlpatterns += (
    path('pwabuilder-sw.js', views.ServiceWorker),
    path('offline.html', views.OfflineApp),
    path('manifest.webmanifest', views.manifestwebmanifest),
)

# For static files
urlpatterns += (
    path('get_static_files_info/', views.get_static_files_info, name='get_static_files_info'),
    # for downloading static files for mobile development
    path('get_static_files/', views.get_static_files, name='get_static_files'),
    # for downloading static files for mobile development
    path('students/singleUserHomePageAPI/', singleUserHomePageJSON, name='singleUserHomePage'),  # for app
    path('students/course/<int:coursepk>/progress', studentCourseProgress, name='studentcourseprogressapp'),  # for app

)

# Login URL get
urlpatterns += (
    path('loaderio-954a872bfd2583affa027425d4a0dd5a/', views.loaderverifylink),
    path('loginforappredirect/<slug:username>/<slug:password>/', views.loginforappredirect, name='loginforappredirect'),
)

# For Media Direct Links

urlpatterns += (
    path('api/v1/video_urlresolver/', views.getDirectURLOfMedias, name='getDirectURLOfMedias'),
    path('api/v1/<int:chapterID>/chat_history/', views.getChatMessageHistoryApi, name='getChatHistory'),
)
