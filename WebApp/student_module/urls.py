from django.contrib.auth.decorators import login_required
from django.urls import path, reverse_lazy

from WebApp.student_module import views
from WebApp.views import ContentsView, NewContentsView
from quiz import views as quizViews
from survey import views as surveyViews
from mail import views as mail_views
from event_calendar import views as cal_views
from survey import views as surv_views

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
    path('forum/create_thread/threadsearchAjax/<int:topic_id>/',
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
         NewContentsView.as_view(), name='student_NewContentViewer'),
)

urlpatterns += (
    path('pageupdateajax/<int:course>/<int:chapter>/',
         views.PageUpdateAjax, name='pageupdateajax'),
    path('studentChapterLogUpdateAjax/<int:chapter>/',
         views.StudentChapterLogUpdateAjax, name='studentChapterLogUpdateAjax'),
)

# Student's Email

urlpatterns += (
    path('mail_list', mail_views.MailListView.as_view(template_name='student_module/mail/index.html'),
         name='student_mail_list'),
    path('mail_outbox', mail_views.MailSendDraftListView.as_view(template_name='student_module/mail/index.html'),
         name='student_mail_send_list'),
    path('mail_starred', mail_views.StarView.as_view(template_name='student_module/mail/star.html'),
         name='student_star_list'),
    path('mail_trashed', mail_views.TrashView.as_view(template_name='student_module/mail/trash.html'),
         name='student_trash_list'),

    path('mail_detail/<int:pk>', mail_views.MailDetailView.as_view(template_name='student_module/mail/detail.html'),
         name='student_mail_detail'),
    path('send_detail/<int:pk>',
         mail_views.SendDetailView.as_view(template_name='student_module/mail/send_detail.html'),
         name='student_send_detail'),
    path('draft_create', mail_views.DraftCreateView.as_view(template_name='student_module/mail/base.html',
                                                            success_url=reverse_lazy('student_mail_send_list')),
         name='student_draft_create'),
    path('mail_draft_detail/<int:pk>', mail_views.DraftToSendView.as_view(template_name='student_module/mail'
                                                                                        '/detail_draft.html',
                                                                          success_url=reverse_lazy(
                                                                              'student_mail_send_list')),
         name='student_mail_draft_detail'),
    path('mail_draft_save/<int:pk>', mail_views.DraftUpdateView.as_view(template_name='student_module/mail'
                                                                                      '/detail_draft.html',
                                                                        success_url=reverse_lazy(
                                                                            'student_mail_send_list')),
         name='student_update_draft'),
    path('mail_delete/<int:pk>', mail_views.MailDeleteView, name='student_mail_delete'),
    path('mail_receiver_delete/<int:pk>',
         mail_views.MailReceiverDeleteView.as_view(success_url=reverse_lazy('student_trash_list')),
         name='student_mail_receiver_delete'),
    path('mail_create', mail_views.MailMultipleCreate.as_view(),
         name='student_mail_create'),
    path('reply_create', mail_views.ReplyCreateView.as_view(template_name="student_module/mail/index.html",
                                                            success_url=reverse_lazy('student_mail_list')),
         name='student_reply_create'),
    path('mail_spam/<int:pk>', mail_views.mail_spam, name='student_mail_spam'),
    path('mail_starred/<int:pk>', mail_views.mail_starred, name='student_mail_starred'),
    path('sender_starred/<int:pk>', mail_views.sender_starred, name='student_sender_starred'),
    path('mail_deleted/<int:pk>', mail_views.mail_deleted, name='student_mail_deleted'),
    path('sender_delete/<int:pk>', mail_views.sender_delete, name='student_sender_delete'),
    path('mail_send/<int:pk>', mail_views.mail_send, name='student_mail_send'),
    path('mail_viewed/<int:pk>', mail_views.mail_viewed, name='student_mail_viewed'),
    path('mail_unread/<int:pk>', mail_views.mail_unread, name='student_mail_unread'),

)

# Student's Calendar
urlpatterns += (
    path('create', cal_views.EventCreateView.as_view(template_name='student_module/calendar/index.html',
                                                     success_url=reverse_lazy('student_event_calendar')),
         name='student_event_calendar_create'),
    path('update/<int:pk>', cal_views.EventUpdateView.as_view(template_name='student_module/calendar/index.html',
                                                              success_url=reverse_lazy('student_event_calendar')),
         name='student_event_calendar_update'),
    path('updated/<int:pk>', cal_views.EventUpdatedView.as_view(template_name='student_module/calendar/index.html',
                                                                success_url=reverse_lazy('student_event_calendar')),
         name='student_event_calendar_updated'),
    path('delete/<int:pk>', cal_views.EventDeleteView.as_view(template_name='student_module/calendar/index.html',
                                                              success_url=reverse_lazy('student_event_calendar')),
         name='student_event_calendar_delete'),
    path('calendar', cal_views.EventListView.as_view(template_name='student_module/calendar/index.html'),
         name='student_event_calendar'),
)


# Student's Survey

# URLS for CategoryInfo
urlpatterns += (

    path('categoryinfo/', surv_views.CategoryInfoListView.as_view(),
         name='student_categoryinfo_list'),
    path('categoryinfo/create/', surv_views.CategoryInfoCreateView.as_view(),
         name='student_categoryinfo_create'),
    path('categoryinfo/detail/<int:pk>/',
         surv_views.CategoryInfoDetailView.as_view(), name='student_categoryinfo_detail'),
    path('categoryinfo/update/<int:pk>/',
         surv_views.CategoryInfoUpdateView.as_view(), name='student_categoryinfo_update'),

)

# urls for SurveyInfo
urlpatterns += (

    path('surveyinfo/', surv_views.SurveyInfoListView.as_view(template_name='student_module/survey/surveylist.html'), name='student_surveyinfo_list'),

    path('surveyinfo/detail/<int:pk>/',
         surv_views.SurveyInfoDetailView.as_view(template_name='student_module/survey/surveyinfo_detail.html'), name='student_surveyinfo_detail'),

    path('surveyinfo/create/', surv_views.SurveyInfoCreateView.as_view(),
         name='student_surveyinfo_create'),

    path('surveyinfo/update/<int:pk>/',
         surv_views.SurveyInfoUpdateView.as_view(), name='student_surveyinfo_update'),

    path('clearsurveys/<int:pk>/',
         surv_views.SurveyclearViewForAdmin, name='student_clearsurveys'),

    path('surveyinfo_ajax/', surv_views.SurveyInfo_ajax.as_view(),
         name='student_surveyinfo_ajax'),
    path('surveyinfo_ajax_update/<int:pk>/', surv_views.SurveyInfoAjaxUpdate.as_view(),
         name='student_surveyinfo_ajax_update'),
    path('surveyinfo_ajax_update_limited/<int:pk>/', surv_views.SurveyInfoAjaxUpdateLimited.as_view(),
         name='student_surveyinfo_ajax_update_limited'),
    path('liveProgressResult/<int:pk>/', surv_views.liveProgressResult.as_view(),
         name='student_liveProgressResult'),

    path('surveyinforetake_ajax/<int:pk>/', surv_views.SurveyInfoRetake_ajax.as_view(),
         name='student_surveyinfo_retake_ajax'),

    path('surveyFilterCategory/', surv_views.surveyFilterCategory.as_view(),
         name='student_surveyFilterCategory'),
)

# urls for QuestionInfo
urlpatterns += (

    path('survey/questioninfo/', surv_views.QuestionInfoListView.as_view(),
         name='student_questioninfo_list'),
    path('survey/questioninfo/create/',
         surv_views.QuestionInfoCreateView.as_view(), name='student_questioninfo_create'),
    path('survey/questioninfo/detail/<int:pk>/',
         surv_views.QuestionInfoDetailView.as_view(), name='student_questioninfo_detail'),
    path('survey/questioninfo/update/<int:pk>/',
         surv_views.QuestionInfoUpdateView.as_view(), name='student_questioninfo_update'),
)

# urls for OptionInfo
urlpatterns += (

    path('optioninfo/', surv_views.OptionInfoListView.as_view(), name='student_optioninfo_list'),
    path('optioninfo/create/', surv_views.OptionInfoCreateView.as_view(),
         name='student_optioninfo_create'),
    path('optioninfo/detail/<int:pk>/',
         surv_views.OptionInfoDetailView.as_view(), name='student_optioninfo_detail'),
    path('optioninfo/update/<int:pk>/',
         surv_views.OptionInfoUpdateView.as_view(), name='student_optioninfo_update'),
)

# urls for SubmitSurvey
urlpatterns += (

    path('submitsurvey/', surv_views.SubmitSurveyListView.as_view(),
         name='student_submitsurvey_list'),
    path('submitsurvey/create/', surv_views.SubmitSurveyCreateView.as_view(),
         name='student_submitsurvey_create'),
    path('submitsurvey/detail/<int:pk>/',
         surv_views.SubmitSurveyDetailView.as_view(), name='student_submitsurvey_detail'),
    path('submitsurvey/update/<int:pk>/',
         surv_views.SubmitSurveyUpdateView.as_view(), name='student_submitsurvey_update'),
)

# urls for AnswerInfo
urlpatterns += (
    path('answerinfo/', surv_views.AnswerInfoListView.as_view(), name='student_answerinfo_list'),
    path('answerinfo/create/', surv_views.AnswerInfoCreateView.as_view(),
         name='student_answerinfo_create'),
    path('answerinfo/detail/<int:pk>/',
         surv_views.AnswerInfoDetailView.as_view(), name='student_answerinfo_detail'),
    path('answerinfo/update/<int:pk>/',
         surv_views.AnswerInfoUpdateView.as_view(), name='student_answerinfo_update'),
)

# delete survey
urlpatterns += (
    path('surveyinfo/delete/', surv_views.deleteSurvey, name='student_surveyinfo_delete'),
)
