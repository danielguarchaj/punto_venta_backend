from django.urls import path, include
from rest_framework import routers

from inventory import views

app_name = 'inventory'

router = routers.DefaultRouter()

router.register('purchases', views.PurchaseViewSet, basename='purchases')

urlpatterns = [
    path('', include(router.urls)),
    path('products/', views.ProductListView.as_view(), name='products'),
    path('purchase-items/', views.PurchaseItemListView.as_view(),
         name='purchase_item_list'),
    path('new-purchase/', views.NewPurchaseAPIView.as_view(), name='new-purchase'),
    path('new-sale/', views.NewSaleAPIView.as_view(), name='new-sale'),
]
