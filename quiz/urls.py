from django.urls import path, include
from rest_framework import routers

from quiz import views
from . import api

try:
    from django.conf.urls import url
except ImportError:
    from django.urls import re_path as url, path

from .views import QuizListView, QuizCreateView, CategoriesListView, \
    QuizUserProgressView, \
    QuizTake, MCQuestionCreateView, TFQuestionCreateView, MCQuestionUpdateView, TFQuestionUpdateView, \
    QuizDetailView, QuizUpdateView, QuizDeleteView, QuizMarkingList, QuizMarkingDetail, SAQuestionCreateView, \
    SAQuestionUpdateView, UpdateQuizBasicInfo, CreateQuizAjax

router = routers.DefaultRouter()
router.register(r'quiz', api.QuizViewSet)
router.register(r'mcquestion', api.MCQuestionViewSet)
router.register(r'tfquestion', api.TFQuestionViewSet)
router.register(r'saquestion', api.SAQuestionViewSet)
router.register(r'answer', api.AnswerViewSet)
router.register(r'progress', api.ProgressViewSet)
router.register(r'sitting', api.SittingViewSet)

urlpatterns = (
    # urls for Django Rest Framework API
    path('api/v1/', include(router.urls)),

    # url(r'^$', view=QuizListView.as_view(), name='quiz_index'),

    url(r'^category/$', view=CategoriesListView.as_view(),
        name='quiz_category_list_all'),

    # url(r'^category/(?P<category_name>[\w|\W-]+)/$', view=ViewQuizListByCategory.as_view(),
    #     name='quiz_category_list_matching'),

    url(r'^progress/$', view=QuizUserProgressView.as_view(), name='quiz_progress'),

    url(r'^marking/$', view=QuizMarkingList.as_view(), name='quiz_marking'),

    url(r'^marking/$', view=QuizMarkingList.as_view(), name='quiz_marking'),

        url(r'^markingfilter/(?P<Quiz_Id>[\d.]+)/$', view=views.FilterMarkingForTeachers, name='markingfilter'),

    url(r'^marking/(?P<pk>[\d.]+)/$', view=QuizMarkingDetail.as_view(), name='quiz_marking_detail'),

    # passes variable 'quiz_name' to quiz_take view
    # url(r'^(?P<slug>[\w-]+)/$', view=QuizDetailView.as_view(), name='quiz_start_page'),

    url(r'^(?P<quiz_name>[\w-]+)/take/$',
        view=QuizTake.as_view(), name='quiz_question'),
)

urlpatterns += (

    path('', QuizListView.as_view(), name='quiz_list'),
    # path('create/', QuizCreateView.as_view(), name='quiz_create'),
    path('create/', CreateQuizAjax.as_view(), name='quiz_create_ajax'),
    path('update/<int:pk>/', QuizUpdateView.as_view(), name='quiz_update'),
    path('update_info/<int:pk>/', UpdateQuizBasicInfo.as_view(),
         name='quiz_update_info'),
    path('detail/<int:pk>/', QuizDetailView.as_view(), name='quiz_detail'),

    path('detail/<slug>/', QuizDetailView.as_view(), name='quiz_detail_s'),
    path('delete/<int:pk>/', QuizDeleteView, name='quiz_delete'),

    path('mcquestion/', views.MCQuestionListView.as_view(), name='mcquestion_list'),
    path('mcquestion/create/', MCQuestionCreateView.as_view(),
         name='mcquestion_create'),
    path('mcquestion/update/<int:pk>',
         MCQuestionUpdateView.as_view(), name='mcquestion_update'),
    path('mcquestion/detail/<int:pk>/',
         views.MCQuestionDetailView.as_view(), name='mcquestion_detail'),
    path('mcquestion/delete/<int:pk>/',
         views.MCQuestionDeleteView, name='mcquestion_delete'),
    path('mcquestion/remove_link/<int:quiz_id>/<int:qn_id>/', views.RemoveMcqLink.as_view(),
         name='mcquestion_remove_link'),

    path('tfquestion/', views.TFQuestionListView.as_view(), name='tfquestion_list'),
    path('tfquestion/create/', TFQuestionCreateView.as_view(),
         name='tfquestion_create'),
    path('tfquestion/update/<int:pk>',
         TFQuestionUpdateView.as_view(), name='tfquestion_update'),
    path('tfquestion/detail/<int:pk>/',
         views.TFQuestionDetailView.as_view(), name='tfquestion_detail'),
    path('tfquestion/delete/<int:pk>/',
         views.TFQuestionDeleteView, name='tfquestion_delete'),
    path('tfquestion/remove_link/<int:quiz_id>/<int:qn_id>/', views.RemoveTfqLink.as_view(),
         name='tfquestion_remove_link'),

    path('saquestion/', views.SAQuestionListView.as_view(), name='saquestion_list'),
    path('saquestion/create/', SAQuestionCreateView.as_view(),
         name='saquestion_create'),
    path('saquestion/update/<int:pk>',
         SAQuestionUpdateView.as_view(), name='saquestion_update'),
    path('saquestion/detail/<int:pk>/',
         views.SAQuestionDetailView.as_view(), name='saquestion_detail'),
    path('saquestion/delete/<int:pk>/',
         views.SAQuestionDeleteView, name='saquestion_delete'),
    path('saquestion/remove_link/<int:quiz_id>/<int:qn_id>/', views.RemoveSaqLink.as_view(),
         name='saquestion_remove_link'),

    path('quizfw/', views.QuizCreateWizard.as_view(), name='quizfw'),
    path('get_course_chapter/', views.GetCourseChapter.as_view(),
         name='get_course_chapter'),
    path('activate_quiz/<int:pk>/',
         views.ActivateQuiz.as_view(), name='activate_quiz'),
    path('deactivate_quiz/<int:pk>/',
         views.DeactivateQuiz.as_view(), name='deactivate_quiz'),

    path('update_questions/<int:pk>/',
         views.UpdateQuestions.as_view(), name='update_questions'),

    path('choose_mcq/<int:pk>/',
         views.QuizMCQChoosePrevious.as_view(), name='choose_mcq'),
    path('choose_tfq/<int:pk>/',
         views.QuizTFQChoosePrevious.as_view(), name='choose_tfq'),
    path('choose_saq/<int:pk>/',
         views.QuizSAQChoosePrevious.as_view(), name='choose_saq'),

    path('quiz/exam_list/', views.QuizExamListView.as_view(),
         name='quiz_exam_list'),

    
)
