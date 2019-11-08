import django_filters
from django_filters.rest_framework import FilterSet

from survey.models import SurveyInfo


class SurveyFilter(FilterSet):
    End_Date_lte = django_filters.DateTimeFilter(field_name="End_Date", lookup_expr='lte')

    class Meta:
        model = SurveyInfo
        fields = ['End_Date_lte']
