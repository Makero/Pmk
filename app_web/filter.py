import django_filters
from app_web import models


class ArticleDateFilter(django_filters.rest_framework.FilterSet):
    """ 文章时间段查询 """
    min_date = django_filters.DateFilter(field_name='create_time__date', lookup_expr='gte')
    max_date = django_filters.DateFilter(field_name='create_time__date', lookup_expr='lte')

    class Meta:
        model = models.Article
        fields = ('min_date', 'max_date')


class MoodDateFilter(django_filters.rest_framework.FilterSet):
    """ 心情时间段查询 """
    min_date = django_filters.DateFilter(field_name='create_time__date', lookup_expr='gte')
    max_date = django_filters.DateFilter(field_name='create_time__date', lookup_expr='lte')

    class Meta:
        model = models.Mood
        fields = ('min_date', 'max_date')