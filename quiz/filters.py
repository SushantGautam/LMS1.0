from django_filters import rest_framework as filters

from quiz.models import Quiz, Answer


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass


class QuizFilter(filters.FilterSet):
    id_in = NumberInFilter(field_name='id', lookup_expr='in')

    class Meta:
        model = Quiz
        fields = ['id_in', 'course_code']


class AnswerFilter(filters.FilterSet):
    question_in = NumberInFilter(field_name='question', lookup_expr='in')

    class Meta:
        model = Answer
        fields = ['question_in', ]
