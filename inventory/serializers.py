from rest_framework import serializers
from inventory.models import Product, Purchase, PurchaseItem
from users.serializers import UserSerializer


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        depth = 1


class PurchaseSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Purchase
        fields = "__all__"


class PurchaseItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = PurchaseItem
        fields = "__all__"


class PurchaseWithDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    purchase_items = PurchaseItemSerializer(many=True)

    class Meta:
        model = Purchase
        fields = "__all__"
