import django_filters
from api.models import Product

class ProductFilter(django_filters.FilterSet):
  class Meta:
    model = Product
    fields = {
      #'name': ['exact', 'contains'], 
      'name': ['iexact', 'icontains'], #iexact is case-insensitive exact match, icontains is case-insensitive contains
      'price': ['exact', 'lt', 'gt', 'range']
    }