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
    SAQuestionUpdateView, MCQuestionCreateFromQuiz, TFQuestionCreateFromQuiz, SAQuestionCreateFromQuiz, \
    MCQuestionUpdateFromQuiz, TFQuestionUpdateFromQuiz, SAQuestionUpdateFromQuiz

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


    #url(r'^$', view=QuizListView.as_view(), name='quiz_index'),

    url(r'^category/$', view=CategoriesListView.as_view(), name='quiz_category_list_all'),

    # url(r'^category/(?P<category_name>[\w|\W-]+)/$', view=ViewQuizListByCategory.as_view(),
    #     name='quiz_category_list_matching'),

    url(r'^progress/$', view=QuizUserProgressView.as_view(), name='quiz_progress'),

    url(r'^marking/$', view=QuizMarkingList.as_view(), name='quiz_marking'),

    url(r'^marking/(?P<pk>[\d.]+)/$', view=QuizMarkingDetail.as_view(), name='quiz_marking_detail'),

    # passes variable 'quiz_name' to quiz_take view
    #url(r'^(?P<slug>[\w-]+)/$', view=QuizDetailView.as_view(), name='quiz_start_page'),

    url(r'^(?P<quiz_name>[\w-]+)/take/$', view=QuizTake.as_view(), name='quiz_question'),
)

urlpatterns += (

    path('', QuizListView.as_view(), name='quiz_list'),
    path('create/', QuizCreateView.as_view(), name='quiz_create'),
    path('update/<int:pk>', QuizUpdateView.as_view(), name='quiz_update'),
    path('detail/<int:pk>', QuizDetailView.as_view(), name='quiz_detail'),
    path('detail/<slug>', QuizDetailView.as_view(), name='quiz_detail_s'),
    path('delete/<int:pk>', QuizDeleteView, name='quiz_delete'),   

    path('mcquestion/', views.MCQuestionListView.as_view(), name='mcquestion_list'),
    path('mcquestion/create/', MCQuestionCreateView.as_view(), name='mcquestion_create'),
    path('mcquestion/create/<int:quiz_id>/', MCQuestionCreateFromQuiz.as_view(), name='mcquestion_create_from_quiz'),
    path('mcquestion/update/<int:pk>', MCQuestionUpdateView.as_view(), name='mcquestion_update'),
    path('mcquestion/update/<int:pk>/<int:quiz_id>', MCQuestionUpdateFromQuiz.as_view(), name='mcquestion_update_from_quiz'),
    path('mcquestion/detail/<int:pk>/', views.MCQuestionDetailView.as_view(), name='mcquestion_detail'),
    path('mcquestion/delete/<int:pk>/', views.MCQuestionDeleteView, name='mcquestion_delete'),

    path('tfquestion/', views.TFQuestionListView.as_view(), name='tfquestion_list'),
    path('tfquestion/create/', TFQuestionCreateView.as_view(), name='tfquestion_create'),
    path('tfquestion/create/<int:quiz_id>/', TFQuestionCreateFromQuiz.as_view(), name='tfquestion_create_from_quiz'),
    path('tfquestion/update/<int:pk>', TFQuestionUpdateView.as_view(), name='tfquestion_update'),
    path('tfquestion/update/<int:pk>/<int:quiz_id>', TFQuestionUpdateFromQuiz.as_view(), name='tfquestion_update_from_quiz'),
    path('tfquestion/detail/<int:pk>/', views.TFQuestionDetailView.as_view(), name='tfquestion_detail'),
    path('tfquestion/delete/<int:pk>/', views.TFQuestionDeleteView, name='tfquestion_delete'),

    path('saquestion/', views.SAQuestionListView.as_view(), name='saquestion_list'),
    path('saquestion/create/', SAQuestionCreateView.as_view(), name='saquestion_create'),
    path('saquestion/create/<int:quiz_id>/', SAQuestionCreateFromQuiz.as_view(), name='saquestion_create_from_quiz'),
    path('saquestion/update/<int:pk>', SAQuestionUpdateView.as_view(), name='saquestion_update'),
    path('saquestion/update/<int:pk>/<int:quiz_id>', SAQuestionUpdateFromQuiz.as_view(), name='saquestion_update_from_quiz'),
    path('saquestion/detail/<int:pk>/', views.SAQuestionDetailView.as_view(), name='saquestion_detail'),
    path('saquestion/delete/<int:pk>/', views.SAQuestionDeleteView, name='saquestion_delete'),

)
