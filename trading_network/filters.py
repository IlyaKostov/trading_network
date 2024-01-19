from django_filters import rest_framework as filters

from trading_network.models import Link


class LinkFilter(filters.FilterSet):
    country = filters.CharFilter(field_name='contact__country', lookup_expr='exact', label='Country')

    class Meta:
        model = Link
        fields = ['country']
