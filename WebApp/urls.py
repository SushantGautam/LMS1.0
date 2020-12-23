# from django.contrib.auth.views import login, logout
from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = (
    # urls for Profile
    path('profile/', views.ProfileView, name='user_profile'),
    #     path('editprofile/', login_required(views.editprofile), name='user_editprofile'),

    # Common url and views for all account for profile edit functions
    path('editprofile/basicinfo', login_required(views.edit_basic_info_ajax),
         name="edit_basic_info_ajax"),
    path('editprofile/contactinfo', login_required(views.edit_contact_info_ajax),
         name="edit_contact_info_ajax"),
    path('editprofile/descriptioninfo', login_required(views.edit_description_info_ajax),
         name="edit_description_info_ajax"),
    path('editprofile/upload_image', login_required(views.edit_profile_image_ajax),
         name="edit_profile_image_ajax"),

    path('profile/change-password/', views.PasswordChangeView.as_view(
        template_name='registration/change_password.html'), name="centeradmin_change_password"),
    path('change-password/<int:pk>/', views.change_password_others),
)

urlpatterns += (
    # urls for CenterInfo
    path('centerinfo/', login_required(views.CenterInfoListView.as_view()),
         name='centerinfo_list'),
    path('centerinfo/create/', login_required(views.CenterInfoCreateView.as_view()),
         name='centerinfo_create'),
    path('centerinfo/detail/<int:pk>/',
         views.CenterInfoDetailView.as_view(), name='centerinfo_detail'),
    path('centerinfo/update/<int:pk>/',
         views.CenterInfoUpdateView.as_view(), name='centerinfo_update'),
    path('centerinfo/delete/<int:pk>/',
         views.CenterInfoDeleteView, name='centerinfo_delete'),
    # url(r'^deletethread/(?P<pk>\d+)/$', views.thread_delete, name='smart_forum_thread_delete'),

)

urlpatterns += (
    # urls for DepartmentInfo
    path('departmentinfo/', login_required(views.DepartmentInfoListView.as_view()),
         name='departmentinfo_list'),
    path('departmentinfo/create/', login_required(views.DepartmentInfoCreateView.as_view()),
         name='departmentinfo_create'),
    path('departmentinfo/create/ajax/', login_required(views.DepartmentInfoCreateViewAjax.as_view()),
         name='departmentinfo_create_ajax'),
    path('departmentinfo/detail/<int:pk>/',
         views.DepartmentInfoDetailView.as_view(), name='departmentinfo_detail'),
    path('departmentinfo/update/<int:pk>/',
         views.DepartmentInfoUpdateView.as_view(), name='departmentinfo_update'),
    path('departmentinfo/update/<int:pk>/ajax/',
         views.DepartmentInfoUpdateViewAjax.as_view(), name='departmentinfo_update_ajax'),
    path('departmentinfo/delete/<int:pk>/',
         views.DepartmentInfoDeleteView, name='departmentinfo_delete'),
)

urlpatterns += (
    # urls for MemberInfo
    path('memberinfo/', views.MemberInfoListView.as_view(), name='memberinfo_list'),
    path('memberinfoajax/', views.MemberInfoListViewAjax.as_view(), name='memberinfo_listajax'),
    # path('memberinfoajax/', views.MemberInfoListViewAjax.as_view(), name='memberinfo_listajax'),
    path('memberinfo/inactive', views.MemberInfoListViewInactive.as_view(),
         name='memberinfo_list_inactive'),
    path('memberinfo/activate/<int:pk>/',
         views.MemberInfoActivate, name='memberinfo_activate'),
    path('memberinfo/deactivate/<int:pk>/',
         views.MemberInfoDeactivate, name='memberinfo_deactivate'),
    path('memberinfo/create/', views.MemberInfoCreateView.as_view(),
         name='memberinfo_create'),
    path('memberinfo/detail/<int:pk>/',
         views.MemberInfoDetailView.as_view(), name='memberinfo_detail'),
    path('memberinfo/update/<int:pk>/',
         views.MemberInfoUpdateView.as_view(), name='memberinfo_update'),
    path('memberinfo/delete/<int:pk>/',
         views.MemberInfoDeleteView.as_view(), name='memberinfo_delete'),
    path('memberinfo/delete/checked/',
         views.MemberInfoDeleteViewChecked, name='memberinfo_delete_checked'),
    path('memberinfo/inactive/delete/checked/',
         views.MemberInfoDeleteViewChecked, name='memberinfo_inactive_delete_checked'),
    path('memberinfo/update/checked/',
         views.MemberInfoEditViewChecked, name='memberinfo_edit_checked'),
    path('memberinfo/inactive/update/checked/',
         views.MemberInfoEditViewChecked, name='memberinfo_inactive_edit_checked'),
    path('importcsvajax', views.ImportCsvFile, name='csv_import_ajax'),
)

urlpatterns += (
    # urls for CourseInfo
    path('courseinfo/', views.CourseInfoListView.as_view(), name='courseinfo_list'),
    path('courseinfo/active/', views.CourseInfoListView.as_view(), name='courseinfo_list_active'),
    path('courseinfo/inactive/', views.CourseInfoListView.as_view(), name='courseinfo_list_inactive'),
    path('courseinfo/create/', views.CourseInfoCreateView.as_view(),
         name='courseinfo_create'),
    path('courseinfo/<int:pk>/', views.CourseInfoDetailView.as_view(),
         name='courseinfo_detail'),
    path('courseinfo/edit/<int:pk>/',
         views.CourseInfoUpdateView.as_view(), name='courseinfo_update'),
    path('courseinfo/delete/<int:pk>/',
         views.CourseInfoDeleteView, name='courseinfo_delete'),
    path('importcsvcourse', views.ImportCourse, name='csv_import_course'),

)

urlpatterns += (
    # urls for ChapterInfo
    path('chapterinfo/create/ajax', views.ChapterInfoCreateViewAjax.as_view(),
         name='chapterinfo_create_ajax'),
    path('chapterinfo/update/<int:pk>/ajax/', views.PartialChapterInfoUpdateViewAjax.as_view(),
         name='partialchapterinfo_update_ajax'),
    path('courseinfo/<int:course>/chapterinfo/',
         views.ChapterInfoListView.as_view(), name='chapterinfo_list'),
    path('courseinfo/<int:course>/create/',
         views.ChapterInfoCreateView.as_view(), name='chapterinfo_create'),
    path('courseinfo/<int:course>/chapterinfo/<int:pk>/', views.ChapterInfoDetailView.as_view(),
         name='chapterinfo_detail'),
    path('courseinfo/<int:course>/chapterinfo/<int:pk>/edit/', views.ChapterInfoUpdateView.as_view(),
         name='chapterinfo_update'),
    path('courseinfo/<int:course>/forum/',
         views.CourseForum, name='Course_Forum'),
    path('change_quiz_test/', views.Changestate.as_view(), name='change_quiz_test'),
    path('chapterinfo/delete/<int:pk>/',
         views.ChapterInfoDeleteView.as_view(), name='chapterinfo_delete'),

    path('courseinfo/<int:course>/chapterinfo/<int:pk>/discussion/', views.ChapterInfoDiscussionView.as_view(),
         name='chapterinfo_discussion'),
    path('chapter/inninginfomap/', views.ChapterInningInfoMappingView, name='chapterinninginfomap'),
)

urlpatterns += (
    # urls for Assignmentinfo
    path('assignmentinfo/create/ajax', views.AssignmentInfoCreateViewAjax.as_view(),
         name='assignmentinfo_create_ajax'),
    path('chapter/<int:chapterpk>/assignmentinfo/create/ajax/', views.AssignmentInfoCreateViewAjax.as_view(),
         name='assignmentinfo_create_ajax_chapter_id'),
    path('courseinfo/<int:course>/chapterinfo/<int:chapter>/assignmentinfo/', views.AssignmentInfoListView.as_view(),
         name='assignmentinfo_list'),
    path('courseinfo/<int:course>/chapterinfo/<int:chapter>/assignmentinfo/create/',
         views.AssignmentInfoCreateView.as_view(), name='assignmentinfo_create'),
    path('courseinfo/<int:course>/chapterinfo/<int:chapter>/assignmentinfo/detail/<int:pk>/',
         views.AssignmentInfoDetailView.as_view(), name='assignmentinfo_detail'),
    path('courseinfo/<int:course>/chapterinfo/<int:chapter>/assignmentinfo/update/<int:pk>/',
         views.AssignmentInfoUpdateView.as_view(), name='assignmentinfo_update'),
    path('assignmentinfo/edit/<int:pk>/ajax/', views.AssignmentInfoEditViewAjax.as_view(),
         name='assignmentinfo_edit_ajax'),
    path('chapter/<int:chapterpk>/assignmentinfo/edit/<int:pk>/ajax/', views.AssignmentInfoEditViewAjax.as_view(),
         name='assignmentinfo_edit_ajax_chapter_id'),
    path('assignmentinfo/<int:pk>/',
         views.AssignmentInfoDeleteView.as_view(), name='assignmentinfo_delete'),
    path('assignment/inninginfomap/', views.AssignmentInningInfoMappingView, name='assignmentinninginfomap'),
)

urlpatterns += (
    # urls for QuestionInfo
    path('courseinfo/<int:course>/chapterinfo/<int:chapter>/assignmentinfo/<int:assignment>/questioninfo/',
         views.QuestionInfoListView.as_view(),
         name='webapp_questioninfo_list'),
    path('courseinfo/<int:course>/chapterinfo/<int:chapter>/assignmentinfo/<int:assignment>/questioninfo/create/',
         views.QuestionInfoCreateView.as_view(),
         name='webapp_questioninfo_create'),
    path(
        'courseinfo/<int:course>/chapterinfo/<int:chapter>/assignmentinfo/<int:assignment>/questioninfo/detail/<int:pk>/',
        views.QuestionInfoDetailView.as_view(), name='webapp_questioninfo_detail'),
    path(
        'courseinfo/<int:course>/chapterinfo/<int:chapter>/assignmentinfo/<int:assignment>/questioninfo/update/<int:pk>/',
        views.QuestionInfoUpdateView.as_view(), name='webapp_questioninfo_update'),
    path('questioninfo/create/ajax',
         views.QuestionInfoCreateViewAjax.as_view(), name='questioninfo_create_ajax'),
    path('assignmentinfo/<int:assignment>/questioninfo/delete/<int:pk>/',
         views.QuestionInfoDeleteView.as_view(), name='webapp_questioninfo_delete'),
    path('questioninfo/edit/<int:pk>/ajax/', views.QuestionInfoEditViewAjax.as_view(),
         name='webapp_questioninfo_edit_ajax'),

)

urlpatterns += (
    # urls for AssignHomeworkInfo
    path('inninginfo/<int:session>/assignmentinfo/<int:assignment>/assignassignmentinfo/',
         views.AssignAssignmentInfoListView.as_view(),
         name='assignassignmentinfo_list'),
    path('inninginfo/<int:session>/assignmentinfo/<int:assignment>/assignassignmentinfo/create/',
         views.AssignAssignmentInfoCreateView.as_view(),
         name='assignassignmentinfo_create'),
    path('inninginfo/<int:session>/assignmentinfo/<int:assignment>/assignassignmentinfo/detail/<int:pk>/',
         views.AssignAssignmentInfoDetailView.as_view(),
         name='assignassignmentinfo_detail'),
    path('inninginfo/<int:session>/assignmentinfo/<int:assignment>/assignassignmentinfo/update/<int:pk>/',
         views.AssignAssignmentInfoUpdateView.as_view(),
         name='assignassignmentinfo_update'),
)

urlpatterns += (
    # urls for AssignAnswerInfo
    path('questioninfo/<int:questioncode>/assignanswerinfo/', views.AssignAnswerInfoListView.as_view(),
         name='assignanswerinfo_list'),
    path('questioninfo/<int:questioncode>/assignanswerinfo/create/', views.AssignAnswerInfoCreateView.as_view(),
         name='assignanswerinfo_create'),
    path('questioninfo/<int:questioncode>/assignanswerinfo/detail/<int:pk>/',
         views.AssignAnswerInfoDetailView.as_view(), name='assignanswerinfo_detail'),
    path('questioninfo/<int:questioncode>/assignanswerinfo/update/<int:pk>/',
         views.AssignAnswerInfoUpdateView.as_view(), name='assignanswerinfo_update'),
    path('deleteassignanswer/',
         views.AssignAnswerInfoDelete, name='assignanswerinfo_delete'),
)

urlpatterns += (
    # urls for InningInfo
    path('sessioninfopopup/create/', views.SessionInfoCreateViewPopup.as_view(),
         name='sessioninfoformpopup'),
    path('groupmappinginfopopup/create/', views.GroupMappingCreateViewPopup.as_view(),
         name='groupmappinginfoformpopup'),
    path('inninggrouppopup/create/', views.InningGroupCreateViewPopup.as_view(),
         name='inninggroupformpopup')

)

urlpatterns += (
    # urls for InningInfo
    path('sessioninfo/', views.SessionInfoListView.as_view(),
         name='sessioninfo_list'),
    path('sessioninfo/create/', views.SessionInfoCreateView.as_view(),
         name='sessioninfo_create'),
    path('sessioninfo/<int:pk>/',
         views.SessionInfoDetailView.as_view(), name='sessioninfo_detail'),
    path('sessioninfo/delete/<int:pk>/',
         views.SessionInfoDeleteView, name='sessioninfo_delete'),
    path('sessioninfo/update/<int:pk>/',
         views.SessionInfoUpdateView.as_view(), name='sessioninfo_update'),
)

urlpatterns += (
    # urls for InningInfo
    path('inninginfo/inactive', views.InningInfoListViewInactive.as_view(),
         name='inninginfo_list_inactive'),
    path('inninginfo/', views.InningInfoListView.as_view(), name='inninginfo_list'),
    path('inninginfo/create/', views.InningInfoCreateView.as_view(),
         name='inninginfo_create'),
    path('inninginfo/saveasnew/<int:pk>/', views.InningInfoCreateView.as_view(),
         name='inninginfo_saveasnew'),
    path('inninginfo/<int:pk>/',
         views.InningInfoDetailView.as_view(), name='inninginfo_detail'),
    path('inninginfo/update/<int:pk>/',
         views.InningInfoUpdateView.as_view(), name='inninginfo_update'),
    path('innninginfo/delete/<int:pk>/',
         views.InningInfoDeleteView, name='inninginfo_delete'),
    path('innninginfo/delete/checked/',
         views.InningInfoDeleteViewChecked, name='inninginfo_delete_checked'),
    path('innninginfo/inactive/delete/checked/',
         views.InningInfoDeleteViewChecked, name='inninginfo_inactive_delete_checked'),
    path('innninginfo/update/checked/',
         views.InningInfoEditViewChecked, name='inninginfo_edit_checked'),
    path('innninginfo/inactive/update/checked/',
         views.InningInfoEditViewChecked, name='inninginfo_inactive_edit_checked'),

    path('inninginfo/csv_import', views.ImportSession, name='csv_import_inninginfo')

)

urlpatterns += (
    # urls for InningGroup
    path('inninggroup/', views.InningGroupListView.as_view(),
         name='inninggroup_list'),
    path('inninggroup/create/', views.InningGroupCreateView.as_view(),
         name='inninggroup_create'),
    path('inninggroup/detail/<int:pk>/',
         views.InningGroupDetailView.as_view(), name='inninggroup_detail'),
    path('inninggroup/update/<int:pk>/',
         views.InningGroupUpdateView.as_view(), name='inninggroup_update'),
    path('inninggroup/delete/<int:pk>/',
         views.InningGroupDeleteView, name='inninggroup_delete'),
    path('inninggroup/csv_import', views.CourseAllocationCSVImport, name='csv_import_inninggroup')
)

urlpatterns += (
    # urls for GroupMapping
    path('groupmapping/', views.GroupMappingListView.as_view(),
         name='groupmapping_list'),
    path('groupmapping/create/', views.GroupMappingCreateView.as_view(),
         name='groupmapping_create'),
    path('groupmapping/saveasnew/<int:pk>/', views.GroupMappingCreateView.as_view(),
         name='groupmapping_saveasnew'),
    path('groupmapping/<int:pk>/',
         views.GroupMappingDetailView.as_view(), name='groupmapping_detail'),
    path('groupmapping/update/<int:pk>/',
         views.GroupMappingUpdateView.as_view(), name='groupmapping_update'),
    path('groupmapping/delete/<int:pk>/',
         views.GroupMappingDeleteView, name='groupmapping_delete'),
    path('groupmapping/csv_import', views.GroupMappingCSVImport, name='csv_import_student_group')

    # path('admin/jsi18n', i18n.javascript_catalog),
)

urlpatterns += (
    path('calendar/', views.calendar, name="admin_calendar"),
)

urlpatterns += (
    path('question/', views.question, name="question"),
)

urlpatterns += (
    path('polls/', views.polls, name="polls"),
)

urlpatterns += (
    # urls for MessageInfo
    path('messageinfo/', views.MessageInfoListView.as_view(),
         name='messageinfo_list'),
    path('messageinfo/create/', views.MessageInfoCreateView.as_view(),
         name='messageinfo_create'),
    path('messageinfo/detail/<int:pk>/',
         views.MessageInfoDetailView.as_view(), name='messageinfo_detail'),
    path('messageinfo/update/<int:pk>/',
         views.MessageInfoUpdateView.as_view(), name='messageinfo_update'),
)

urlpatterns += (
    # urls for Ajax
    path('inninginfo/create/ajax',
         views.InningInfoCreateSessionAjax.as_view(), name='sessioninfo_create_ajax'),
    path('groupmapping/create/ajax',
         views.GroupCreateSessionAjax.as_view(), name='group_create_ajax'),
    path('inninggroup/create/ajax',
         views.InningGroupCreateAjax.as_view(), name='inninggroup_create_ajax'),
)

urlpatterns += (
    # urls for chapterpagebuilder
    path('courseinfo/<int:course>/chapterinfo/<int:chapter>/chapterpagebuilder',
         views.chapterpagebuilder, name='chapterpagebuilder'),

    path('courseinfo/<int:course>/chapterinfo/<int:chapter>/ChapterBuilder',
         views.newChapterBuilder, name='newChapterBuilder'),

    path('viewchapter',
         views.chapterviewer, name='chapterviewer'),
    path('saveFile', views.save_file, name='saveFile'),
    path('saveVideo', views.save_video, name='saveVideo'),
    path('save3d', views.save_3d_file, name='save3d'),
    path('saveJson', views.save_json, name='saveJson'),
    path('export/<int:course>/<int:chapter>/',
         views.export_chapter, name='exportzip'),
    path('import', views.import_chapter, name='importzip'),
#     path('courseinfo/<int:course>/chapterinfo/<int:chapter>/contents',
#          views.ContentsView.as_view(), name='contentviewer'),
    path('courseinfo/<int:course>/chapterinfo/<int:chapter>/contents',
         views.NewContentsView.as_view(), name='NewContentViewer'),
    # path('courseinfo/<int:course>/chapterinfo/<int:chapter>/offline_contents',
    #     views.OfflineContentsView.as_view(), name='offlinecontentviewer'),
#     path('courseinfo/<int:course>/chapterinfo/<int:chapter>/contents/preview',
#          views.ContentsView.as_view(), name='previewcontentviewer'),
    path('courseinfo/<int:course>/chapterinfo/<int:chapter>/contents/preview',
         views.NewContentsView.as_view(), name='newpreviewcontentviewer'),
    path('delete-chapter-files',
         views.deletechapterfile, name='delete-chapter-files'),
    path('retrieve-chapter-files',
         views.retrievechapterfile, name='retrieve-chapter-files'),
    path('checkMediaFiles/', views.checkForMediaFiles, name='checkMediaFiles'),
)

urlpatterns += (
    path('AchievementPage_Student/<int:student_id>', views.AchievementPage_Student,
         name='AchievementPage_Student'),
    path('AchievementPage_All', views.AchievementPage_All,
         name='AchievementPage_All'),
    path('AchievementPage_All_Ajax/<int:Inningsfilter>/<slug:studentfilter>/<int:CourseFilter>/',
         views.AchievementPage_All_Ajax,
         name='AchievementPage_All_Ajax'),

)

# url patterns for session manager
urlpatterns += (
    path('inninginfo/<int:pk>/sessionmanager/update/', views.SessionManagerUpdateView.as_view(),
         name='session-manager-update'),
)

urlpatterns += (
    path('attendance/<int:attend_date>/<int:courseid>/<int:teacherid>/', views.viewteacherAttendance,
         name='teacherattendanceview'),
)

# Course Progress

urlpatterns += (
    path('courseinfo/detail/<int:coursepk>/progress/',
         views.CourseProgressView, name='admin_course_progress'),
    path('courseinfo/detail/<int:coursepk>/inning/<inningpk>/progress/',
         views.CourseProgressView, name='admin_course_progress_withinning'),
    path('courseinfo/detail/<int:courseid>/progress/<int:chapterid>/<int:studentid>',
         views.StudentChapterProgressView, name='student_chapter_progress'),
    path('editstudentChapterProgressTime/<int:chapterid>/<int:studentid>/', views.editStudentChapterProgressTime,
         name="editStudentChapterProgressTime"),
    path('courseinfo/detail/<int:coursepk>/<int:sessionpk>/download/', views.CourseProgressDownload,
         name="progress_download")
)

# Notice URL

urlpatterns += (
    path('notice_view_create', views.notice_view_create, name='notice_view_create'),
)

urlpatterns += (
    path('meet/<int:userid>/<slug:meetcode>/',
         views.MeetPublic, name='public-meet'),
)

urlpatterns += (
    path('course/progress/download/<int:teacher_pk>',
         views.progress_download, name='course_progress_download'),
)

urlpatterns += (
    path('teacher_report/', views.TeacherReport.as_view(), name='teacher_report'),
    path('teacher_report/<int:teacherpk>/<int:coursepk>/', views.TeacherIndividualReport.as_view(),
         name='teacher_individual_report'),
    path('teacher_report/downloadchapterdata', views.DownloadChapterData, name='donwload')
)

urlpatterns += (
    path('storageinfo/', views.getMediaInformation, name='storageinfo'),
)