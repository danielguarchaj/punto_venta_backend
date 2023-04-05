from rest_framework import generics
from inventory.models import Purchase, PurchaseItem
from inventory.serializers import PurchaseSerializer, PurchaseItemSerializer
from inventory.filters import PurchaseItemFilter, PurchaseFilter


class PurchaseListView(generics.ListAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    filterset_class = PurchaseFilter


class PurchaseItemListView(generics.ListAPIView):
    queryset = PurchaseItem.objects.all()
    serializer_class = PurchaseItemSerializer
    filterset_class = PurchaseItemFilter
