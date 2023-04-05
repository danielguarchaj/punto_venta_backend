from django.urls import path
from inventory.views import PurchaseListView, PurchaseItemListView

app_name = 'inventory'

urlpatterns = [
    path('purchases/', PurchaseListView.as_view(), name='purchase_list'),
    path('purchase-items/', PurchaseItemListView.as_view(),
         name='purchase_item_list'),
]
