from django.contrib.auth.decorators import login_required
from django.urls import path

from WebApp.student_module import views
from WebApp.views import ContentsView, NewContentsView
from quiz import views as quizViews
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
    path('profile/change-password/', views.PasswordChangeView.as_view(
        template_name='student_module/change_password_student.html'), name='student_change_password'),

)

urlpatterns += (
    # urls for CourseInfo
    #     path('courseinfo/', views.CourseInfoListView.as_view(),
    #          name='student_courseinfo_list'),
    path('courseinfo/mycourses', views.MyCoursesListView.as_view(),
         name='student_mycourses_list'),
    path('courseinfo/detail/forum/<int:course>',
         views.CourseForum, name='Student_Course_Forum'),
    path('courseinfo/detail/<int:pk>/', views.CourseInfoDetailView.as_view(),
         name='student_courseinfo_detail'),
)

urlpatterns += (
    # urls for ChapterInfo
    path('courseinfo/<int:course>/chapterinfo/',
         views.ChapterInfoListView.as_view(), name='student_chapterinfo_list'),
    path('courseinfo/<int:course>/chapterinfo/<int:pk>/', views.ChapterInfoDetailView.as_view(),
         name='student_chapterinfo_detail'),
)

urlpatterns += (
    # urls for AssignmentInfo
    path('courseinfo/<int:course>/chapterinfo/<int:chapter>/assignmentinfo/<int:pk>/',
         views.AssignmentInfoDetailView.as_view(),
         name='student_assignmentinfo_detail'),
    path('myassignments/', views.MyAssignmentsListView.as_view(),
         name='student_myassignmentinfo_list')
)

urlpatterns += (
    # urls for AssignAnswerInfo
    path('assignanswerinfo/create', views.submitAnswer.as_view(),
         name='assignanswerinfo_create_ajax'),
    # path('questioninfo/<int:questioncode>/assignanswerinfo/create/', views.AssignAnswerInfoCreateView.as_view(),
    #      name='assignanswerinfo_create'),
    # path('questioninfo/<int:questioncode>/assignanswerinfo/detail/<int:pk>/',
    #      views.AssignAnswerInfoDetailView.as_view(), name='assignanswerinfo_detail'),
    # path('questioninfo/<int:questioncode>/assignanswerinfo/update/<int:pk>/',
    #      views.AssignAnswerInfoUpdateView.as_view(), name='assignanswerinfo_update'),
)
urlpatterns += (
    # urls for Profile
    path('profile/', login_required(views.ProfileView),
         name='student_user_profile'),
    path('editprofile_student/', login_required(views.student_editprofile),
         name='student_user_editprofile'),

)

# urlpatterns += (
#     path('questions_student/', views.questions_student, name="questions_student"),
# )
urlpatterns += (
    # urls for SurveyInfo
    path('questions_student/', views.questions_student.as_view(),
         name='questions_student'),

    path('questions_student_detail/detail/<int:pk>/',
         views.questions_student_detail.as_view(), name='questions_student_detail'),

    path('questions_student_detail_history/detail/<int:pk>/',
         views.questions_student_detail_history.as_view(), name='questions_student_detail_history'),

    path('surveyinfo_ajax/', surveyViews.SurveyInfo_ajax.as_view(),
         name='surveyinfo_ajax'),

    path('ParticipateSurvey/', views.ParticipateSurvey.as_view(),
         name='ParticipateSurvey'),

    path('surveyFilterCategory_student/', views.surveyFilterCategory_student.as_view(),
         name='surveyFilterCategory_student'),

)

urlpatterns += (
    path('forum/', views.Index.as_view(), name="student_forum"),
    path('forum/create_thread', views.create_thread,
         name="student_create_thread"),
    path('forum/create_thread/(?P<nodegroup_pk>\d+)/',
         views.create_thread, name='student_create_thread'),
    path('forum/create_thread/(?P<nodegroup_pk>\d+)/(?P<topic_pk>\d+)/',
         views.create_thread, name='student_create_thread'),

    path('forum/edit/<int:pk>/', views.edit_thread, name='student_edit_thread'),
    path('forum/create_topic/(?P<student_nodegroup_pk>\d+)/',
         views.create_topic, name='student_create_topic'),

    path('forum/create_topic', views.create_topic, name="student_create_topic"),
    path('forum/search/(?P<keyword>.*)',
         views.SearchView.as_view(), name='student_search'),
    path('forum/search/', views.search_redirect,
         name='student_search_redirect'),
    path('forum/nodegroup/<int:pk>/',
         views.NodeGroupView.as_view(), name='student_nodegroup'),
    path('forum/thread/<int:pk>/',
         views.ThreadView.as_view(), name='student_thread'),
    path('forum/ThreadListLoadMoreViewAjax/<int:pk>/<int:count>',
         views.ThreadList_LoadMoreViewAjax, name='Load_More'),
    path('forum/topic/<int:pk>/', views.TopicView.as_view(), name='student_topic'),
    path('forum/info/<int:pk>/', views.user_info, name='student_info'),
    path('forum/posts/<int:pk>/', views.UserPosts.as_view(), name='student_posts'),
    path('forum/threads/<int:pk>/',
         views.UserThreads.as_view(), name='student_threads'),
    path('forum/notification', views.NotificationView.as_view(),
         name='student_notification'),
    path('forum/create_thread/threadsearchAjax/<int:topic_id>/<slug:threadkeywordList>/',
         views.ThreadSearchAjax, name='thread_search_student'),
    path('quiz/progress/<int:pk>/', views.QuizUserProgressDetailView.as_view(),
         name='student_progress_detail'),
    path('quiz/progress', views.QuizUserProgressView.as_view(),
         name='student_progress'),
    path('quiz/progress_history/<int:quiz>/', views.QuizUserProgressHistoryView.as_view(),
         name='student_progress_history'),
    path('quiz/exam_list/', quizViews.QuizExamListView.as_view(),
         name='student_quiz_exam_list'),
)

urlpatterns += (
    path('courseinfo/<int:course>/chapterinfo/<int:chapter>/contents',
         ContentsView.as_view(), name='student_contentviewer'),
    path('courseinfo/<int:course>/chapterinfo/<int:chapter>/newcontents',
         NewContentsView.as_view(), name='NewContentViewer'),
)

urlpatterns += (
    path('pageupdateajax/<int:course>/<int:chapter>/',
         views.PageUpdateAjax, name='pageupdateajax'),
    path('studentChapterLogUpdateAjax/<int:chapter>/',
         views.StudentChapterLogUpdateAjax, name='studentChapterLogUpdateAjax'),
)
