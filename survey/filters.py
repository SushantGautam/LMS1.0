import django_filters
from django_filters.rest_framework import FilterSet

from survey.models import SurveyInfo


class SurveyFilter(FilterSet):
    End_Date_gte = django_filters.DateTimeFilter(field_name="End_Date", lookup_expr='gte')
    Start_Date_lte = django_filters.DateTimeFilter(field_name="Start_Date", lookup_expr='lte')

    class Meta:
        model = SurveyInfo
        fields = ['End_Date_gte','Start_Date_lte', "Course_Code"]