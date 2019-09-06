from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.urls import path

from WebApp.teacher_module import views
from WebApp.teacher_module.views import CourseInfoListView

urlpatterns = (
    # urls for TodoTInfo
    path('', login_required(views.start), name='teacher_home'),
)
urlpatterns += (
    # urls for CourseInfo
    path('courseinfo/', views.CourseInfoListView.as_view(),
         name='teacher_courseinfo_list'),
    path('courseinfo/create/', views.CourseInfoCreateView.as_view(),
         name='teacher_courseinfo_create'),
    path('courseinfo/detail/<int:pk>/', views.CourseInfoDetailView.as_view(),
         name='teacher_courseinfo_detail'),
    path('courseinfo/update/<int:pk>/', views.CourseInfoUpdateView.as_view(),
         name='teacher_courseinfo_update'),
)

urlpatterns += (
    # urls for ChapterInfo
    path('chapterinfo/', views.ChapterInfoListView.as_view(),
         name='teacher_chapterinfo_list'),
    path('chapterinfo/create/', views.ChapterInfoCreateView.as_view(),
         name='teacher_chapterinfo_create'),
    path('chapterinfo/build/', views.ChapterInfoBuildView,
         name='teacher_chapterinfo_build'),

    path('chapterinfo/detail/<int:pk>/', views.ChapterInfoDetailView.as_view(),
         name='teacher_chapterinfo_detail'),
    path('chapterinfo/update/<int:pk>/', views.ChapterInfoUpdateView.as_view(),
         name='teacher_chapterinfo_update'),
)

urlpatterns += (
    # urls for Profile
    path('profile/', login_required(views.ProfileView),
         name='teacher_user_profile'),

)

urlpatterns += (
    # urls for Profile
    path('makequery/', login_required(views.makequery), name='teacher_makequery'),

)

urlpatterns += (
    path('question_teachers/', views.question_teachers, name="question_teachers"),
)

urlpatterns += (
    path('polls_teachers/', views.polls_teachers, name="polls_teachers"),
)
