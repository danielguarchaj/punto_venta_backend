from functools import reduce
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from inventory.models import Purchase, PurchaseItem, Product, SaleInvoice, SaleInvoiceItem
from inventory.serializers import PurchaseSerializer, PurchaseItemSerializer, PurchaseWithDetailSerializer, ProductSerializer
from inventory.filters import PurchaseItemFilter, PurchaseFilter
from customers.models import Customer

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
            quantity = float(purchaseItem['quantity'])
            product = Product.objects.get(pk=purchaseItem['productId'])
            product.increment_stock(int(quantity))
            PurchaseItem.objects.create(
                purchase=newPurchase,
                product=product,
                expiration_date=purchaseItem['expirationDate'] if purchaseItem['expirationDate'] else None,
                price=float(purchaseItem['price']),
                quantity=quantity,
            )
        return Response({"status": 200})


class NewSaleAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        saleList = request.data['saleList']
        totalSale = 0
        customerId = request.data['customerId']
        customer = Customer.objects.get(
            pk=customerId) if customerId is not None else None
        for sale in saleList:
            soldProduct = Product.objects.get(pk=sale['productId'])
            subTotal = float(soldProduct.sale_price) * float(sale['quantity'])
            totalSale += subTotal

        newSaleInvoice = SaleInvoice.objects.create(
            user=user,
            customer=customer,
            total=totalSale,
        )

        for sale in saleList:
            product = Product.objects.get(pk=sale['productId'])
            product.decrement_stock(sale['quantity'])
            SaleInvoiceItem.objects.create(
                sale_invoice=newSaleInvoice,
                product=product,
                quantity=float(sale['quantity'])
            )

        return Response({"status": 200})
