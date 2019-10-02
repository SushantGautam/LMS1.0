from django.contrib.auth.decorators import login_required
from django.urls import path

from WebApp.teacher_module import views

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
    # urls for TodoTInfo
     path('groupmappinginfo/<int:pk>/', views.GroupMappingDetailViewTeacher.as_view(),
          name='teacher_groupmapping_detail'),
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
    path('assignment_answers/<int:pk>', views.AssignmentAnswers.as_view(),
         name='teacher_assignment_answers'),
)

urlpatterns += (
    # urls for Profile
    path('profile/', login_required(views.ProfileView),
         name='teacher_user_profile'),
    path('editprofile_teacher/', login_required(views.teacher_editprofile),
         name='teacher_user_editprofile'),
)

urlpatterns += (
    # urls for Profile
    path('makequery/', login_required(views.makequery), name='teacher_makequery'),

)

urlpatterns += (
    path('question_teachers/', views.SurveyInfoListView.as_view(),
         name="question_teachers"),
    # path('surveyinfo/create/', views.SurveyInfoCreateView.as_view(),
    #          name='surveyinfo_create'),
    path('polls_teachers/', views.polls_teachers, name='polls_teachers'),
    path('polls_teachers/detail/<int:pk>/',
         views.TeacherSurveyInfoDetailView.as_view(), name='polls_teachers'),
    path('teacherSurveyFilterCategory/', views.teacherSurveyFilterCategory.as_view(),
         name='teacherSurveyFilterCategory'),
    path('TeacherSurveyInfo_ajax/', views.TeacherSurveyInfo_ajax.as_view(),
         name='TeacherSurveyInfo_ajax'),
)

urlpatterns += (
    path('forum/', views.Index.as_view(), name="teacher_forum"),
    path('forum/create_thread', views.create_thread, name="teacher_forum_create"),
    path('forum/create_thread/(?P<nodegroup_pk>\d+)/',
         views.create_thread, name='teacher_forum_create'),
    path('forum/create_thread/(?P<teacher_nodegroup_pk>\d+)/(?P<teacher_topic_pk>\d+)/',
         views.create_thread, name='teacher_forum_create'),


    path('forum/create_topic/(?P<teacher_nodegroup_pk>\d+)/',
         views.create_topic, name='teacher_create_topic'),

    path('forum/create_topic', views.create_topic, name="teacher_create_topic"),
    path('forum/search/(?P<keyword>.*)',
         views.SearchView.as_view(), name='teacher_search'),
    path('forum/search/', views.search_redirect,
         name='teacher_search_redirect'),
    path('forum/nodegroup/<int:pk>/',
         views.NodeGroupView.as_view(), name='teacher_nodegroup'),
    path('forum/thread/<int:pk>/',
         views.ThreadView.as_view(), name='teacher_thread'),
    path('forum/topic/<int:pk>/', views.TopicView.as_view(), name='teacher_topic'),
    path('forum/info/<int:pk>/', views.user_info, name='teacher_info'),
    path('forum/posts/<int:pk>/', views.UserPosts.as_view(), name='teacher_posts'),
    path('forum/threads/<int:pk>/',
         views.UserThreads.as_view(), name='teacher_threads'),
    path('forum/notification', views.NotificationView.as_view(),
         name='teacher_notification'),
)

urlpatterns += (
    # urls for Quiz
    path('quiz/', views.QuizListView.as_view(),
         name='teacher_quiz_list'),
    path('quiz/create/', views.QuizCreateView.as_view(),
         name='teacher_quiz_create'),
    path('quiz/detail/<int:pk>/', views.QuizDetailView.as_view(),
         name='teacher_quiz_detail'),
    path('quiz/edit/<int:pk>/', views.QuizUpdateView.as_view(),
         name='teacher_quiz_update'),
    path('detail/<slug>', views.QuizDetailView.as_view(),
         name='teacher_quiz_detail_s'),

    path('mcquestion/', views.MCQuestionListView.as_view(),
         name='teacher_mcquestion_list'),
    path('mcquestion/create/', views.MCQuestionCreateView.as_view(),
         name='teacher_mcquestion_create'),
    path('mcquestion/create/<int:quiz_id>/', views.MCQuestionCreateFromQuiz.as_view(),
         name='teacher_mcquestion_create_from_quiz'),
    path('mcquestion/update/<int:pk>', views.MCQuestionUpdateView.as_view(),
         name='teacher_mcquestion_update'),
    path('mcquestion/update/<int:pk>/<int:quiz_id>', views.MCQuestionUpdateFromQuiz.as_view(),
         name='teacher_mcquestion_update_from_quiz'),
    path('mcquestion/detail/<int:pk>/', views.MCQuestionDetailView.as_view(),
         name='teacher_mcquestion_detail'),
    path('mcquestion/delete/<int:pk>/', views.MCQuestionDeleteView,
         name='teacher_mcquestion_delete'),

    path('tfquestion/', views.TFQuestionListView.as_view(),
         name='teacher_tfquestion_list'),
    path('tfquestion/create/', views.TFQuestionCreateView.as_view(),
         name='teacher_tfquestion_create'),
    path('tfquestion/create/<int:quiz_id>/', views.TFQuestionCreateFromQuiz.as_view(),
         name='teacher_tfquestion_create_from_quiz'),
    path('tfquestion/update/<int:pk>', views.TFQuestionUpdateView.as_view(),
         name='teacher_tfquestion_update'),
    path('tfquestion/update/<int:pk>/<int:quiz_id>', views.TFQuestionUpdateFromQuiz.as_view(),
         name='teacher_tfquestion_update_from_quiz'),
    path('tfquestion/detail/<int:pk>/', views.TFQuestionDetailView.as_view(),
         name='teacher_tfquestion_detail'),
    path('tfquestion/delete/<int:pk>/', views.TFQuestionDeleteView,
         name='teacher_tfquestion_delete'),

    path('saquestion/', views.SAQuestionListView.as_view(),
         name='teacher_saquestion_list'),
    path('saquestion/create/', views.SAQuestionCreateView.as_view(),
         name='teacher_saquestion_create'),
    path('saquestion/create/<int:quiz_id>/', views.SAQuestionCreateFromQuiz.as_view(),
         name='teacher_saquestion_create_from_quiz'),
    path('saquestion/update/<int:pk>', views.SAQuestionUpdateView.as_view(),
         name='teacher_saquestion_update'),
    path('saquestion/update/<int:pk>/<int:quiz_id>', views.SAQuestionUpdateFromQuiz.as_view(),
         name='teacher_saquestion_update_from_quiz'),
    path('saquestion/detail/<int:pk>/', views.SAQuestionDetailView.as_view(),
         name='teacher_saquestion_detail'),
    path('saquestion/delete/<int:pk>/', views.SAQuestionDeleteView,
         name='teacher_saquestion_delete'),

    path('quiz/quizfw/', views.QuizCreateWizard.as_view(), name='teacher_quizfw'),
    path('quiz/marking/', views.QuizMarkingList.as_view(), name='teacher_quiz_marking'),
    path('quiz/marking/<int:pk>/', views.QuizMarkingDetail.as_view(), name='teacher_quiz_marking_detail'),
)
