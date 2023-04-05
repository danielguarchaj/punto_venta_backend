from django_filters import rest_framework as filters, DateFromToRangeFilter
from inventory.models import PurchaseItem, Purchase


class PurchaseFilter(filters.FilterSet):
  purchase_date = DateFromToRangeFilter()
  class Meta:
    model = Purchase
    fields = {
      'user__username': ["icontains"],
    }


class PurchaseItemFilter(filters.FilterSet):
  expiration_date = DateFromToRangeFilter()
  class Meta:
    model = PurchaseItem
    fields = {
      
      'product__name': ["icontains"],
      'product__description': ["icontains"],
      'product__category__name': ["icontains"],
      'product__category__description': ["icontains"],
      'product__brand__name': ["icontains"],
      'product__brand__description': ["icontains"],
    }