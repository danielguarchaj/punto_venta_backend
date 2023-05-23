from functools import reduce
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from inventory.models import (
    Purchase,
    PurchaseItem,
    Product,
    SaleInvoice,
    SaleInvoiceItem,
    Provider,
)
from inventory.serializers import (
    PurchaseSerializer,
    PurchaseItemSerializer,
    PurchaseWithDetailSerializer,
    ProductSerializer,
    ProviderSerializer,
    SaleInvoiceWithDetailSerializer,
)
from inventory.filters import PurchaseItemFilter, PurchaseFilter, SaleInvoiceFilter
from customers.models import Customer


class PurchaseViewSet(ModelViewSet):
    queryset = Purchase.objects.all()
    filterset_class = PurchaseFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return PurchaseWithDetailSerializer
        return PurchaseSerializer


class SaleInvoiceViewSet(ModelViewSet):
    queryset = SaleInvoice.objects.all()
    filterset_class = SaleInvoiceFilter
    serializer_class = SaleInvoiceWithDetailSerializer


class PurchaseItemListView(generics.ListAPIView):
    queryset = PurchaseItem.objects.all()
    serializer_class = PurchaseItemSerializer
    filterset_class = PurchaseItemFilter


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProviderListView(generics.ListAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer


class NewPurchaseAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        purchaseList = request.data['purchaseList']
        providerId = request.data['providerId']
        provider = Provider.objects.get(pk=providerId)
        total = reduce(
            lambda x, y: x + (float(y['price']) * float(y['quantity'])), purchaseList, 0)
        newPurchase = Purchase.objects.create(
            user=user,
            total=total,
            provider=provider,
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


class VoidPurchase(APIView):
    def post(self, request):
        purchase_id = request.data['purchaseId']
        purchase = Purchase.objects.get(pk=purchase_id)
        purchase.void_purchase()
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
                quantity=float(sale['quantity']),
                total=float(sale['quantity'] * product.sale_price)
            )

        return Response({"status": 200})


class VoidSale(APIView):
    def post(self, request):
        import time
        time.sleep(3)
        sale_id = request.data['saleId']
        sale = SaleInvoice.objects.get(pk=sale_id)
        sale.void_sale()
        return Response({"status": 200})