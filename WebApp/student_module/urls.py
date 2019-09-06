from django.conf.urls import url
from django.urls import path
from django.contrib.auth.decorators import login_required

from WebApp.student_module import views
from survey import views as surveyViews
#
# urlpatterns = (
#     # urls for TodoTInfo
#     path('', login_required(views.start), name='student_home'),
# )
#
#
#

# from django.urls import path
# from . import views

urlpatterns = (
    # urls for TodoTInfo
    path('', login_required(views.start), name='student_home'),
)

urlpatterns += (
    # path('mycourse/', views.mycourse, name="students_mycourse"),
    path('quiz/', views.quiz, name="students_quiz"),
    path('quizzes/', views.quizzes, name="quiz_question"),
    path('calendar/', views.calendar, name="students_calendar"),

)

urlpatterns += (
    # urls for CourseInfo
    path('courseinfo/', views.CourseInfoListView.as_view(),
         name='student_courseinfo_list'),
    path('courseinfo/mycourses', views.MyCoursesListView.as_view(),
         name='student_mycourses_list'),
    path('courseinfo/detail/<int:pk>/', views.CourseInfoDetailView.as_view(),
         name='student_courseinfo_detail'),
)

urlpatterns += (
    # urls for ChapterInfo
    path('courseinfo/<int:course>/chapterinfo/', views.ChapterInfoListView.as_view(), name='student_chapterinfo_list'),
    path('courseinfo/<int:course>/chapterinfo/<int:pk>/', views.ChapterInfoDetailView.as_view(),
         name='student_chapterinfo_detail'),
)

urlpatterns += (
    # urls for AssignmentInfo
    path('courseinfo/<int:course>/chapterinfo/<int:chapter>/assignmentinfo/<int:pk>/',
    views.AssignmentInfoDetailView.as_view(),
        name='student_assignmentinfo_detail'),
    path('myassignments/',views.MyAssignmentsListView.as_view(), name='student_myassignmentinfo_list')
)

urlpatterns += (
    # urls for Profile
    path('profile/', login_required(views.ProfileView),
         name='student_user_profile'),
)

# urlpatterns += (
#     path('questions_student/', views.questions_student, name="questions_student"),
# )
urlpatterns += (
    # urls for SurveyInfo
    path('questions_student/', views.questions_student.as_view(), name='questions_student'),

    path('questions_student_detail/detail/<int:pk>/',
         views.questions_student_detail.as_view(), name='questions_student_detail'),

     # path('surveyinfo/detail', views.get_survey_info,
     #     name='get_survey_info'),

    path('surveyinfo_ajax/', surveyViews.SurveyInfo_ajax.as_view(),
        name='surveyinfo_ajax'),
    
    path('ParticipateSurvey/', views.ParticipateSurvey.as_view(),
        name='ParticipateSurvey'),
)

# urlpatterns += (
#     path('polls_student/', views.polls_student, name="polls_student"),
# )

# urlpatterns += (
#     path('polls_student_view/', views.polls_student_view,
#          name="polls_student_view"),
# )
