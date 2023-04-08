from django.urls import path
from inventory import views

app_name = 'inventory'

urlpatterns = [
    path('products/', views.ProductListView.as_view(), name='products'),
    path('purchases/', views.PurchaseListView.as_view(), name='purchase_list'),
    path('purchases/<int:pk>/', views.PurchaseRetrieveView.as_view(),
         name='purchase_detail'),
    path('purchase-items/', views.PurchaseItemListView.as_view(),
         name='purchase_item_list'),
    path('new-purchase/', views.NewPurchaseAPIView.as_view(), name='new-purchase')
]
