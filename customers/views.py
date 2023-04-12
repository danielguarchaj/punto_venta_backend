from rest_framework import generics
from customers.models import Customer
from customers.serializers import CustomerSerializer
from customers.filters import CustomerFilter

class CustomerListView(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filterset_class = CustomerFilter