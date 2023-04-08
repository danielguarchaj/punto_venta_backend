from functools import reduce
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from inventory.models import Purchase, PurchaseItem, Product
from inventory.serializers import PurchaseSerializer, PurchaseItemSerializer, PurchaseWithDetailSerializer, ProductSerializer
from inventory.filters import PurchaseItemFilter, PurchaseFilter

from time import sleep

class PurchaseListView(generics.ListAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    filterset_class = PurchaseFilter


class PurchaseRetrieveView(generics.RetrieveAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseWithDetailSerializer


class PurchaseItemListView(generics.ListAPIView):
    queryset = PurchaseItem.objects.all()
    serializer_class = PurchaseItemSerializer
    filterset_class = PurchaseItemFilter


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class NewPurchaseAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        purchaseList = request.data
        total = reduce(
            lambda x, y: x + (float(y['price']) * float(y['quantity'])), purchaseList, 0)
        newPurchase = Purchase.objects.create(
            user=user,
            total=total
        )
        for purchaseItem in purchaseList:
            PurchaseItem.objects.create(
                purchase=newPurchase,
                product=Product.objects.get(pk=purchaseItem['productId']),
                expiration_date=purchaseItem['expirationDate'] if purchaseItem['expirationDate'] else None,
                price=float(purchaseItem['price']),
                quantity=float(purchaseItem['quantity']),
            )
        sleep(3)
        return Response({"status": 200})
