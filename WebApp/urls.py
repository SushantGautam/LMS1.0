from django.conf.urls import url
# from django.contrib.auth.views import login, logout
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from rest_framework import routers

from . import api
from . import views



urlpatterns = (
    # urls for Profile
    path('profile/', views.ProfileView, name='user_profile'),
#     path('editprofile/', login_required(views.editprofile), name='user_editprofile'),
    
    # Common url and views for all account for profile edit functions 
    path('editprofile/basicinfo', login_required(views.edit_basic_info_ajax), name="edit_basic_info_ajax"),
    path('editprofile/contactinfo', login_required(views.edit_contact_info_ajax), name="edit_contact_info_ajax"),
    path('editprofile/descriptioninfo', login_required(views.edit_description_info_ajax), name="edit_description_info_ajax"),
    path('editprofile/upload_image', login_required(views.edit_profile_image_ajax), name="edit_profile_image_ajax"),

    path('profile/change-password/', views.PasswordChangeView.as_view(template_name='registration/change_password.html'), name="centeradmin_change_password"),
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
    # urls for MemberInfo
    path('memberinfo/', views.MemberInfoListView.as_view(), name='memberinfo_list'),
    path('memberinfo/inactive', views.MemberInfoListViewInactive.as_view(), name='memberinfo_list_inactive'),
    path('memberinfo/activate/<int:pk>/', views.MemberInfoActivate, name='memberinfo_activate'),
    path('memberinfo/deactivate/<int:pk>/', views.MemberInfoDeactivate, name='memberinfo_deactivate'),
    path('memberinfo/create/', views.MemberInfoCreateView.as_view(), name='memberinfo_create'),
    path('memberinfo/detail/<int:pk>/', views.MemberInfoDetailView.as_view(), name='memberinfo_detail'),
    path('memberinfo/update/<int:pk>/', views.MemberInfoUpdateView.as_view(), name='memberinfo_update'),
    path('memberinfo/delete/<int:pk>/', views.MemberInfoDeleteView.as_view(), name='memberinfo_delete'),
    path('importcsvajax', views.ImportCsvFile, name='csv_import_ajax'),
)

urlpatterns += (
    # urls for CourseInfo
    path('courseinfo/', views.CourseInfoListView.as_view(), name='courseinfo_list'),
    path('courseinfo/create/', views.CourseInfoCreateView.as_view(), name='courseinfo_create'),
    path('courseinfo/<int:pk>/', views.CourseInfoDetailView.as_view(), name='courseinfo_detail'),
    path('courseinfo/edit/<int:pk>/', views.CourseInfoUpdateView.as_view(), name='courseinfo_update'),
    path('courseinfo/delete/<int:pk>/', views.CourseInfoDeleteView, name='courseinfo_delete'),

)

urlpatterns += (
    # urls for ChapterInfo
    path('chapterinfo/create/ajax', views.ChapterInfoCreateViewAjax.as_view(), name='chapterinfo_create_ajax'),
    path('courseinfo/<int:course>/chapterinfo/', views.ChapterInfoListView.as_view(), name='chapterinfo_list'),
    path('courseinfo/<int:course>/create/', views.ChapterInfoCreateView.as_view(), name='chapterinfo_create'),
    path('courseinfo/<int:course>/chapterinfo/<int:pk>/', views.ChapterInfoDetailView.as_view(),
         name='chapterinfo_detail'),
    path('courseinfo/<int:course>/chapterinfo/<int:pk>/edit/', views.ChapterInfoUpdateView.as_view(),
         name='chapterinfo_update'),
    path('courseinfo/<int:course>/forum/', views.CourseForum, name='Course_Forum'),
    path('change_quiz_test/', views.Changestate.as_view(), name='change_quiz_test'),
    path('chapterinfo/delete/<int:pk>/', views.ChapterInfoDeleteView.as_view(), name='chapterinfo_delete'),

)

urlpatterns += (
    # urls for Assignmentinfo
    path('assignmentinfo/create/ajax', views.AssignmentInfoCreateViewAjax.as_view(), name='assignmentinfo_create_ajax'),

    path('courseinfo/<int:course>/chapterinfo/<int:chapter>/assignmentinfo/', views.AssignmentInfoListView.as_view(),
         name='assignmentinfo_list'),
    path('courseinfo/<int:course>/chapterinfo/<int:chapter>/assignmentinfo/create/',
         views.AssignmentInfoCreateView.as_view(), name='assignmentinfo_create'),
    path('courseinfo/<int:course>/chapterinfo/<int:chapter>/assignmentinfo/detail/<int:pk>/',
         views.AssignmentInfoDetailView.as_view(), name='assignmentinfo_detail'),
    path('courseinfo/<int:course>/chapterinfo/<int:chapter>/assignmentinfo/update/<int:pk>/',
         views.AssignmentInfoUpdateView.as_view(), name='assignmentinfo_update'),
    path('assignmentinfo/edit/ajax', views.AssignmentInfoEditViewAjax.as_view(), name='assignmentinfo_edit_ajax'),
    path('assignmentinfo/<int:pk>/', views.AssignmentInfoDeleteView.as_view(), name='assignmentinfo_delete'),
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
    path('assignmentinfo/<int:assignment>/questioninfo/delete/<int:pk>/', views.QuestionInfoDeleteView.as_view(), name='webapp_questioninfo_delete'),

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
    path('sessioninfo/', views.SessionInfoListView.as_view(), name='sessioninfo_list'),
    path('sessioninfo/create/', views.SessionInfoCreateView.as_view(),
         name='sessioninfo_create'),
    path('sessioninfo/<int:pk>/',
         views.SessionInfoDetailView.as_view(), name='sessioninfo_detail'),
    path('sessioninfo/update/<int:pk>/',
         views.SessionInfoUpdateView.as_view(), name='sessioninfo_update'),
)

urlpatterns += (
    # urls for InningInfo
    path('inninginfo/inactive', views.InningInfoListViewInactive.as_view(), name='inninginfo_list_inactive'),
    path('inninginfo/', views.InningInfoListView.as_view(), name='inninginfo_list'),
    path('inninginfo/create/', views.InningInfoCreateView.as_view(),
         name='inninginfo_create'),
    path('inninginfo/<int:pk>/',
         views.InningInfoDetailView.as_view(), name='inninginfo_detail'),
    path('inninginfo/update/<int:pk>/',
         views.InningInfoUpdateView.as_view(), name='inninginfo_update'),
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
)

urlpatterns += (
    # urls for GroupMapping
    path('groupmapping/', views.GroupMappingListView.as_view(),
         name='groupmapping_list'),
    path('groupmapping/create/', views.GroupMappingCreateView.as_view(),
         name='groupmapping_create'),
    path('groupmapping/<int:pk>/',
         views.GroupMappingDetailView.as_view(), name='groupmapping_detail'),
    path('groupmapping/update/<int:pk>/',
         views.GroupMappingUpdateView.as_view(), name='groupmapping_update'),
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
    path('viewchapter',
         views.chapterviewer, name='chapterviewer'),
    path('saveFile', views.save_file, name='saveFile'),
    path('saveVideo', views.save_video, name='saveVideo'),
    path('saveJson', views.save_json, name='saveJson'),
    path('export/<int:course>/<int:chapter>/', views.export_chapter, name='exportzip'),
    path('import', views.import_chapter, name='importzip'),

)

urlpatterns += (
    # urls for chapterpagebuilder
    path('3DViewer/<path:urlpath>',
         views.ThreeDViewer, name='3DViewer'),
    path('3DViewer/',
         views.ThreeDViewer, name='3DViewer'),
)