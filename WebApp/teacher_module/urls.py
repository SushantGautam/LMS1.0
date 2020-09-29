from django.contrib.auth.decorators import login_required
from django.urls import path, reverse_lazy

from WebApp.teacher_module import views
from quiz import views as quizViews
from survey import views as survey_views
from .. import views as admin_views
from mail import views as mail_views
from event_calendar import views as cal_views
from survey import views as surv_views

urlpatterns = (
    # urls for TodoTInfo
    path('', login_required(views.start), name='teacher_home'),
)
urlpatterns += (
    # urls for CourseInfo
    path('courseinfo/', views.CourseInfoListView.as_view(),
         name='teacher_courseinfo_list'),
    path('courseinfo/mycourses/', views.MyCourseListView.as_view(),
         name='teacher_mycourses_list'),
    path('courseinfo/mycourses/active/', views.MyCourseListView.as_view(),
         name='teacher_mycourses_list_active'),
    path('courseinfo/mycourses/inactive/', views.MyCourseListView.as_view(),
         name='teacher_mycourses_list_inactive'),
    path('courseinfo/create/', views.CourseInfoCreateView.as_view(),
         name='teacher_courseinfo_create'),
    path('courseinfo/detail/<int:pk>/', views.CourseInfoDetailView.as_view(),
         name='teacher_courseinfo_detail'),
    path('courseinfo/detail/forum/<int:course>',
         views.CourseForum, name='Teacher_Course_Forum'),
    path('courseinfo/edit/<int:pk>/', views.CourseInfoUpdateView.as_view(),
         name='teacher_courseinfo_update'),
)
urlpatterns += (
    # urls for TodoTInfo
    path('groupmappinginfo/<int:pk>/', views.GroupMappingDetailViewTeacher.as_view(),
         name='teacher_groupmapping_detail'),
    path('studentInfo/<int:id>/', views.Student_DetailInfo,
         name='Student_DetailInfo'),
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
    path('courseinfo/<int:course>/chapterinfo/<int:chapter>/assignmentinfo/<int:pk>/inning/<int:inningpk>/',
         views.AssignmentInfoDetailView.as_view(),
         name='teacher_assignmentinfo_detail_with_inning'),
    path('courseinfo/<int:course>/chapterinfo/<int:chapter>/assignmentinfo/update/<int:pk>/',
         views.AssignmentInfoUpdateView.as_view(), name='teacher_assignmentinfo_update'),
    path('myassignments/', views.MyAssignmentsListView.as_view(),
         name='teacher_myassignmentinfo_list'),
    path('assignment_answers/<int:pk>/', views.AssignmentAnswers.as_view(),
         name='teacher_assignment_answers'),
    path('assignment_answers/<int:pk>/inning/<int:inningpk>/', views.AssignmentAnswers.as_view(),
         name='teacher_assignment_answers_with_inning'),
    path('assignment_answers/download', views.downloadAssignmentAnswers, name='downloadAssignmentAnswers'),
    path('assignment_answers/download/delete', views.deletedownloadAssignmentAnswers,
         name='deletedownloadAssignmentAnswers'),
    path('assignmentinfo/<int:pk>/', views.AssignmentInfoDeleteView.as_view(),
         name='teacher_assignmentinfo_delete'),
    path('assignmentinfo/<int:assignment>/questioninfo/delete/<int:pk>/',
         views.QuestionInfoDeleteView.as_view(), name='teacher_questioninfo_delete'),
    path('submitStudentscore/<int:Answer_id>/<int:score>/',
         views.submitStudentscore, name='submitStudentscore'),

)

urlpatterns += (
    # urls for Profile
    path('profile/', login_required(views.ProfileView),
         name='teacher_user_profile'),
    #     path('editprofile_teacher/', login_required(views.teacher_editprofile),
    #          name='teacher_user_editprofile'),
    path('profile/change-password/', views.PasswordChangeView.as_view(
        template_name='teacher_module/change_password_teacher.html'), name='teacher_change_password'),
)

urlpatterns += (
    # urls for Profile
    path('makequery/', login_required(views.makequery), name='teacher_makequery'),

)

urlpatterns += (
    path('question_teachers/', views.SurveyInfoListView.as_view(),
         name="question_teachers"),
    # path('question_teachers/', views.question_teachers.as_view(),
    #          name="question_teachers"),
    # path('surveyinfo/create/', views.SurveyInfoCreateView.as_view(),
    #          name='surveyinfo_create'),
    # path('polls_teachers/', views.polls_teachers, name='polls_teachers'),
    path('surveyinfodetail/detail/<int:pk>/',
         views.TeacherSurveyInfoDetailView.as_view(), name='surveyinfodetail'),
    path('surveyFilterCategory/', views.teacherSurveyFilterCategory.as_view(),
         name='teacherSurveyFilterCategory'),
    path('TeacherSurveyInfo_ajax/', views.TeacherSurveyInfo_ajax.as_view(),
         name='TeacherSurveyInfo_ajax'),
    # path('TeacherSurveyInfo_ajax/', survey_views.SurveyInfo_ajax.as_view(),
    #      name='TeacherSurveyInfo_ajax'),
    path('TeacherSurveyInfo_ajax_update/<int:pk>/', survey_views.SurveyInfoAjaxUpdate.as_view(),
         name='TeacherSurveyInfo_ajax_update'),
    path('TeacherSurveyInfo_ajax_update_limited/<int:pk>/', survey_views.SurveyInfoAjaxUpdateLimited.as_view(),
         name='TeacherSurveyInfo_ajax_update_limited'),
    path('surveyinforetake_ajax/<int:pk>/', survey_views.SurveyInfoRetake_ajax.as_view(),
         name='teacher_surveyinfo_retake_ajax'),

)

urlpatterns += (
    path('forum/', views.Index.as_view(), name="teacher_forum"),
    path('forum/create_thread', views.create_thread,
         name="teacher_create_thread"),
    path('forum/create_thread/(?P<nodegroup_pk>\d+)/',
         views.create_thread, name='teacher_create_thread'),
    path('forum/create_thread/(?P<nodegroup_pk>\d+)/(?P<topic_pk>\d+)/',
         views.create_thread, name='teacher_create_thread'),

    path('forum/create_topic/(?P<teacher_nodegroup_pk>\d+)/',
         views.create_topic, name='teacher_create_topic'),

    path('forum/create_topic', views.create_topic, name="teacher_create_topic"),
    path('forum/search/(?P<keyword>.*)',
         views.SearchView.as_view(), name='teacher_search'),
    path('forum/search/', views.search_redirect,
         name='teacher_search_redirect'),
    path('forum/search/(?P<keyword>.*?)/page/(?P<page>[0-9]+)/$',
         views.SearchView.as_view(), name='teacher_search'),
    path('forum/nodegroup/<int:pk>/',
         views.NodeGroupView.as_view(), name='teacher_nodegroup'),
    path('forum/thread/<int:pk>/',
         views.ThreadView.as_view(), name='teacher_thread'),
    path('forum/ThreadListLoadMoreViewAjax/<int:pk>/<int:count>',
         views.ThreadList_LoadMoreViewAjax, name='teacher_Load_More'),
    path('forum/topic/<int:pk>/', views.TopicView.as_view(), name='teacher_topic'),
    path('forum/info/<int:pk>/', views.user_info, name='teacher_info'),
    path('forum/posts/<int:pk>/', views.UserPosts.as_view(), name='teacher_posts'),
    path('forum/threads/<int:pk>/',
         views.UserThreads.as_view(), name='teacher_threads'),
    path('forum/notification', views.NotificationView.as_view(),
         name='teacher_notification'),
    path('forum/edit/<int:pk>/', views.edit_thread, name='teacher_edit_thread'),
    path('forum/create_thread/threadsearchAjax/<int:topic_id>/',
         views.ThreadSearchAjax, name='thread_search'),

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
    path('update_info/<int:pk>/', views.UpdateQuizBasicInfo.as_view(),
         name='teacher_quiz_update_info'),
    path('quiz/exam_list/', quizViews.QuizExamListView.as_view(),
         name='teacher_quiz_exam_list'),
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
    path('activate_quiz/<int:pk>/', quizViews.ActivateQuiz.as_view(),
         name='teacher_activate_quiz'),
    path('deactivate_quiz/<int:pk>/', quizViews.DeactivateQuiz.as_view(),
         name='teacher_deactivate_quiz'),

    # Quiz Marking
    path('quiz/marking/', views.QuizMarkingList.as_view(),
         name='teacher_quiz_marking'),
    path('quiz/marking/<int:quiz_id>', views.QuizMarking.as_view(),
         name='teacher_individual_quiz_marking'),
    path('quiz/marking/detail/<int:pk>/', views.QuizMarkingDetail.as_view(),
         name='teacher_quiz_marking_detail'),
    # URL for quiz marking download    
    path('quiz/marking/exportcsv/<int:quiz_pk>', views.QuizMarkingCSV, name='quiz_marking_csv'),
)

urlpatterns += (
    path('courseinfo/<int:course>/chapterinfo/<int:chapter>/chapterpagebuilder',
         admin_views.chapterpagebuilder, name='teachers_chapterpagebuilder'),
    path('courseinfo/<int:course>/chapterinfo/<int:chapter>/newChapterBuilder',
         admin_views.newChapterBuilder, name='teachers_newChapterBuilder'),
    path('courseinfo/<int:course>/chapterinfo/<int:chapter>/contents',
         admin_views.ContentsView.as_view(), name='teacher_contentviewer'),
    path('courseinfo/<int:course>/chapterinfo/<int:chapter>/newcontents',
         admin_views.NewContentsView.as_view(), name='teacher_NewContentViewer'),
    path('courseinfo/<int:course>/chapterinfo/<int:chapter>/contents/newpreview',
         admin_views.NewContentsView.as_view(), name='teachersnewpreviewcontentviewer'),
)

urlpatterns += (
    path('mysessions/inactive', views.SessionAdminInningInfoListViewInactive.as_view(),
         name='teachers_mysession_list_inactive'),
    path('mysessions/', views.SessionAdminInningInfoListView.as_view(), name='teachers_mysession_list'),
    path('mysessions/<int:pk>/', views.SessionAdminInningInfoDetailView.as_view(), name='teachers_mysession_detail'),

    path('groupmapping/update/<int:pk>/', views.GroupMappingUpdateView.as_view(), name='teachers_groupmapping_update'),
    path('inninggroup/detail/<int:pk>/', views.InningGroupDetailView.as_view(), name='teachers_inninggroup_detail'),
    path('inninggroup/update/<int:pk>/', views.InningGroupUpdateView.as_view(), name='teachers_inninggroup_update'),
    path('inninginfo/update/<int:pk>/', views.InningInfoUpdateView.as_view(), name='teachers_inninginfo_update'),

)
from django.conf.urls import url

urlpatterns += (
    # urls for Attendance
    path('attendance-home/', views.AttendanceListView.as_view(), name='teacher_attendance_list'),
    path('attendance/create/', views.AttendanceCreateView.as_view(), name='teacher_attendance_create'),
    path('attendance/detail/<int:pk>/', views.AttendanceDetailView.as_view(), name='teacher_attendance_detail'),
    path('attendance/update/<int:pk>/', views.AttendanceUpdateView.as_view(), name='teacher_attendance_update'),

    url(r'^attendance/class/(?P<inningpk>\d+)/(?P<course>\d+)/(?P<attend_date>\d{4}-\d{2}-\d{2})/$',
        views.CourseAttendance, name='course_attendance'),
    url(r'^attendance/class-list/(?P<inningpk>\d+)/(?P<course>\d+)/(?P<attend_date>\d{4}-\d{2}-\d{2})/$',
        views.CourseAttendanceList, name='course_attendance_list'),
    url(r'^attendance/class-list/(?P<inningpk>\d+)/(?P<course>\d+)/$', views.CourseAttendanceList,
        name='course_attendance_list_nodate'),

    url(r'^attendance/$', views.CourseAttendanceList, name='attendance'),
    path('courseinfo/detail/<int:course>/attendance/', views.CourseAttendanceList,
         name='teacher_courseinfo_detail_attendance'),

)

# Chapter Progress

urlpatterns += (
    path('courseinfo/<int:course>/chapterinfo/<int:pk>/student_progress/',
         views.chapterStudentProgress, name='chapter_student_progress'),
    path('inninginfo/<int:inningpk>/courseinfo/<int:course>/chapterinfo/<int:pk>/student_progress/',
         views.chapterStudentProgress, name='chapter_student_progress_inning'),

)

# Course Progress

urlpatterns += (
    path('courseinfo/detail/<int:coursepk>/progress/',
         admin_views.CourseProgressView, name='course_progress'),
    path('courseinfo/detail/<int:coursepk>/inning/<inningpk>/progress/',
         admin_views.CourseProgressView, name='course_progress_withinning'),
    path('courseinfo/detail/<int:courseid>/progress/<int:chapterid>/<int:studentid>',
         admin_views.StudentChapterProgressView, name='student_chapter_progress_teacher'),
)

# Teacher's Attendance

urlpatterns += (
    path('courseinfo/detail/<int:courseid>/take-attendance/',
         views.teacherAttendance, name='taketeacherAttendance'),
)

urlpatterns += (
    path('meet/',
         views.Meet, name='teacher-meet'),
)

# Teacher's Email

urlpatterns += (
    path('mail_list', mail_views.MailListView.as_view(template_name='teacher_module/mail/index.html'),
         name='teacher_mail_list'),
    path('mail_outbox', mail_views.MailSendDraftListView.as_view(template_name='teacher_module/mail/index.html'),
         name='teacher_mail_send_list'),
    path('mail_starred', mail_views.StarView.as_view(template_name='teacher_module/mail/star.html'),
         name='teacher_star_list'),
    path('mail_trashed', mail_views.TrashView.as_view(template_name='teacher_module/mail/trash.html'),
         name='teacher_trash_list'),

    path('mail_detail/<int:pk>', mail_views.MailDetailView.as_view(template_name='teacher_module/mail/detail.html'),
         name='teacher_mail_detail'),
    path('send_detail/<int:pk>',
         mail_views.SendDetailView.as_view(template_name='teacher_module/mail/send_detail.html'),
         name='teacher_send_detail'),
    path('draft_create', mail_views.DraftCreateView.as_view(template_name='teacher_module/mail/base.html',
                                                            success_url=reverse_lazy('teacher_mail_send_list')),
         name='teacher_draft_create'),
    path('mail_draft_detail/<int:pk>', mail_views.DraftToSendView.as_view(template_name='teacher_module/mail'
                                                                                        '/detail_draft.html',
                                                                          success_url=reverse_lazy(
                                                                              'teacher_mail_send_list')),
         name='teacher_mail_draft_detail'),
    path('mail_draft_save/<int:pk>', mail_views.DraftUpdateView.as_view(template_name='teacher_module/mail'
                                                                                      '/detail_draft.html',
                                                                        success_url=reverse_lazy(
                                                                            'teacher_mail_send_list')),
         name='teacher_update_draft'),
    path('mail_delete/<int:pk>', mail_views.MailDeleteView, name='teacher_mail_delete'),
    path('mail_receiver_delete/<int:pk>',
         mail_views.MailReceiverDeleteView.as_view(success_url=reverse_lazy('teacher_trash_list')),
         name='teacher_mail_receiver_delete'),
    path('mail_create', mail_views.MailMultipleCreate.as_view(),
         name='teacher_mail_create'),
    path('reply_create', mail_views.ReplyCreateView.as_view(template_name="teacher_module/mail/index.html",
                                                            success_url=reverse_lazy('teacher_mail_list')),
         name='teacher_reply_create'),
    path('mail_spam/<int:pk>', mail_views.mail_spam, name='teacher_mail_spam'),
    path('mail_starred/<int:pk>', mail_views.mail_starred, name='teacher_mail_starred'),
    path('sender_starred/<int:pk>', mail_views.sender_starred, name='teacher_sender_starred'),
    path('mail_deleted/<int:pk>', mail_views.mail_deleted, name='teacher_mail_deleted'),
    path('sender_delete/<int:pk>', mail_views.sender_delete, name='teacher_sender_delete'),
    path('mail_send/<int:pk>', mail_views.mail_send, name='teacher_mail_send'),
    path('mail_viewed/<int:pk>', mail_views.mail_viewed, name='teacher_mail_viewed'),
    path('mail_unread/<int:pk>', mail_views.mail_unread, name='teacher_mail_unread'),

)

# Teacher's Calendar
urlpatterns += (
    path('create', cal_views.EventCreateView.as_view(template_name='teacher_module/calendar/index.html',
                                                     success_url=reverse_lazy('teacher_event_calendar')),
         name='teacher_event_calendar_create'),
    path('update/<int:pk>', cal_views.EventUpdateView.as_view(template_name='teacher_module/calendar/index.html',
                                                              success_url=reverse_lazy('teacher_event_calendar')),
         name='teacher_event_calendar_update'),
    path('updated/<int:pk>', cal_views.EventUpdatedView.as_view(template_name='teacher_module/calendar/index.html',
                                                                success_url=reverse_lazy('teacher_event_calendar')),
         name='teacher_event_calendar_updated'),
    path('delete/<int:pk>', cal_views.EventDeleteView.as_view(template_name='teacher_module/calendar/index.html',
                                                              success_url=reverse_lazy('teacher_event_calendar')),
         name='teacher_event_calendar_delete'),
    path('calendar', cal_views.EventListView.as_view(template_name='teacher_module/calendar/index.html'),
         name='teacher_event_calendar'),
)

# Teacher's Survey

# URLS for CategoryInfo
urlpatterns += (

    path('categoryinfo/', surv_views.CategoryInfoListView.as_view(),
         name='teacher_categoryinfo_list'),
    path('categoryinfo/create/', surv_views.CategoryInfoCreateView.as_view(),
         name='teacher_categoryinfo_create'),
    path('categoryinfo/detail/<int:pk>/',
         surv_views.CategoryInfoDetailView.as_view(), name='teacher_categoryinfo_detail'),
    path('categoryinfo/update/<int:pk>/',
         surv_views.CategoryInfoUpdateView.as_view(), name='teacher_categoryinfo_update'),

)

# urls for SurveyInfo
urlpatterns += (

    path('surveyinfo/', surv_views.SurveyInfoListView.as_view(template_name='teacher_module/survey/surveylist.html'), name='teacher_surveyinfo_list'),

    path('surveyinfo/detail/<int:pk>/',
         surv_views.SurveyInfoDetailView.as_view(template_name='teacher_module/survey/surveyinfo_detail.html'), name='teacher_surveyinfo_detail'),

    path('surveyinfo/create/', surv_views.SurveyInfoCreateView.as_view(),
         name='teacher_surveyinfo_create'),

    path('surveyinfo/update/<int:pk>/',
         surv_views.SurveyInfoUpdateView.as_view(), name='teacher_surveyinfo_update'),

    path('clearsurveys/<int:pk>/',
         surv_views.SurveyclearViewForAdmin, name='teacher_clearsurveys'),

    path('surveyinfo_ajax/', surv_views.SurveyInfo_ajax.as_view(),
         name='teacher_surveyinfo_ajax'),
    path('surveyinfo_ajax_update/<int:pk>/', surv_views.SurveyInfoAjaxUpdate.as_view(),
         name='teacher_surveyinfo_ajax_update'),
    path('surveyinfo_ajax_update_limited/<int:pk>/', surv_views.SurveyInfoAjaxUpdateLimited.as_view(),
         name='teacher_surveyinfo_ajax_update_limited'),
    path('liveProgressResult/<int:pk>/', surv_views.liveProgressResult.as_view(),
         name='teacher_liveProgressResult'),

    path('surveyinforetake_ajax/<int:pk>/', surv_views.SurveyInfoRetake_ajax.as_view(),
         name='teacher_surveyinfo_retake_ajax'),

    path('surveyFilterCategory/', surv_views.surveyFilterCategory.as_view(),
         name='teacher_surveyFilterCategory'),
)

# urls for QuestionInfo
urlpatterns += (

    path('survey/questioninfo/', surv_views.QuestionInfoListView.as_view(),
         name='teacher_questioninfo_list'),
    path('survey/questioninfo/create/',
         surv_views.QuestionInfoCreateView.as_view(), name='teacher_questioninfo_create'),
    path('survey/questioninfo/detail/<int:pk>/',
         surv_views.QuestionInfoDetailView.as_view(), name='teacher_questioninfo_detail'),
    path('survey/questioninfo/update/<int:pk>/',
         surv_views.QuestionInfoUpdateView.as_view(), name='teacher_questioninfo_update'),
)

# urls for OptionInfo
urlpatterns += (

    path('optioninfo/', surv_views.OptionInfoListView.as_view(), name='teacher_optioninfo_list'),
    path('optioninfo/create/', surv_views.OptionInfoCreateView.as_view(),
         name='teacher_optioninfo_create'),
    path('optioninfo/detail/<int:pk>/',
         surv_views.OptionInfoDetailView.as_view(), name='teacher_optioninfo_detail'),
    path('optioninfo/update/<int:pk>/',
         surv_views.OptionInfoUpdateView.as_view(), name='teacher_optioninfo_update'),
)

# urls for SubmitSurvey
urlpatterns += (

    path('submitsurvey/', surv_views.SubmitSurveyListView.as_view(),
         name='teacher_submitsurvey_list'),
    path('submitsurvey/create/', surv_views.SubmitSurveyCreateView.as_view(),
         name='teacher_submitsurvey_create'),
    path('submitsurvey/detail/<int:pk>/',
         surv_views.SubmitSurveyDetailView.as_view(), name='teacher_submitsurvey_detail'),
    path('submitsurvey/update/<int:pk>/',
         surv_views.SubmitSurveyUpdateView.as_view(), name='teacher_submitsurvey_update'),
)

# urls for AnswerInfo
urlpatterns += (
    path('answerinfo/', surv_views.AnswerInfoListView.as_view(), name='teacher_answerinfo_list'),
    path('answerinfo/create/', surv_views.AnswerInfoCreateView.as_view(),
         name='teacher_answerinfo_create'),
    path('answerinfo/detail/<int:pk>/',
         surv_views.AnswerInfoDetailView.as_view(), name='teacher_answerinfo_detail'),
    path('answerinfo/update/<int:pk>/',
         surv_views.AnswerInfoUpdateView.as_view(), name='teacher_answerinfo_update'),
)

# delete survey
urlpatterns += (
    path('surveyinfo/delete/', surv_views.deleteSurvey, name='teacher_surveyinfo_delete'),
)
