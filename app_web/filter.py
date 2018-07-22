import django_filters
from app_web import models


class ArticleDateFilter(django_filters.rest_framework.FilterSet):
    """ 时间段查询 """
    min_date = django_filters.DateFilter(field_name='create_time__date', lookup_expr='gte')
    max_date = django_filters.DateFilter(field_name='create_time__date', lookup_expr='lte')

    class Meta:
        model = models.Article
        fields = ('min_date', 'max_date')
