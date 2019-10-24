from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from  WebApp import views
from django.contrib.auth.decorators import login_required, user_passes_test

from decorator_include import decorator_include
from LMS.decorators import authorize

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^quiz/', include('quiz.urls')),
    # path('', include('WebApp.urls')),
    path('', decorator_include([login_required, authorize(lambda u: u.Is_CenterAdmin)], 'WebApp.urls')),
    url(r'^$', views.start, name='start'),
    path('forum/',include('forum.urls')),
    path('students/',decorator_include([login_required, authorize(lambda u: u.Is_Student)], 'WebApp.student_module.urls')),
    path('teachers/',decorator_include([login_required, authorize(lambda u: u.Is_Teacher)], 'WebApp.teacher_module.urls')),
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
