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
    path('courseinfo/mycourses', views.MyCourseListView.as_view(),
         name='teacher_mycourses_list'),
    path('courseinfo/create/', views.CourseInfoCreateView.as_view(),
         name='teacher_courseinfo_create'),
    path('courseinfo/detail/<int:pk>/', views.CourseInfoDetailView.as_view(),
         name='teacher_courseinfo_detail'),
    path('courseinfo/edit/<int:pk>/', views.CourseInfoUpdateView.as_view(),
         name='teacher_courseinfo_update'),
)

urlpatterns += (
    # urls for ChapterInfo
    path('courseinfo/<int:course>/chapterinfo/', views.ChapterInfoListView.as_view(),
         name='teacher_chapterinfo_list'),
    path('courseinfo/<int:course>/chapterinfo/create/', views.ChapterInfoCreateView.as_view(),
         name='teacher_chapterinfo_create'),
    path('chapterinfo/build/', views.ChapterInfoBuildView,
         name='teacher_chapterinfo_build'),
    path('courseinfo/<int:course>/chapterinfo/<int:pk>/', views.ChapterInfoDetailView.as_view(),
         name='teacher_chapterinfo_detail'),
    path('courseinfo/<int:course>/chapterinfo/<int:pk>/edit/', views.ChapterInfoUpdateView.as_view(),
         name='teacher_chapterinfo_update'),
)

urlpatterns += (
    # urls for AssignmentInfo
    path('courseinfo/<int:course>/chapterinfo/<int:chapter>/assignmentinfo/<int:pk>/',
         views.AssignmentInfoDetailView.as_view(),
         name='teacher_assignmentinfo_detail'),
    path('courseinfo/<int:course>/chapterinfo/<int:chapter>/assignmentinfo/update/<int:pk>/',
         views.AssignmentInfoUpdateView.as_view(), name='teacher_assignmentinfo_update'),
    path('myassignments/', views.MyAssignmentsListView.as_view(),
         name='teacher_myassignmentinfo_list'),
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

urlpatterns += (
    path('forum/', views.Index.as_view(), name="teacher_forum"),
    path('forum/create_thread', views.create_thread, name="teacher_forum_create"),
)
