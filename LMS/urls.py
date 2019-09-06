from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^quiz/', include('quiz.urls')),
    path('', include('WebApp.urls')),
    path('forum/',include('forum.urls')),
    path('students/',include('WebApp.student_module.urls')),
    path('teachers/',include('WebApp.teacher_module.urls')),
    path('survey/',include('survey.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
