import django_filters

from WebApp.models import CourseInfo


class MyCourseFilter(django_filters.FilterSet):
    class Meta:
        model = CourseInfo
        fields = ["Course_Name", ]
