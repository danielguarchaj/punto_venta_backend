from django.db import models
from django.contrib.auth.models import User
from customers.models import Customer
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver


class Brand(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categoria"


class Provider(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def increment_stock(self, amount):
        self.stock = self.stock + amount
        self.save()

    def decrement_stock(self, amount):
        self.stock = self.stock - amount
        self.save()

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, null=True)
    purchase_date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    voided = models.BooleanField(default=False)

    def __str__(self):
        return f'Compra {self.pk} realizada por {self.user.username}'

    def void_purchase(self):
        for purchaseItem in self.purchase_items.all():
            purchaseItem.product.decrement_stock(purchaseItem.quantity)
        self.voided = True
        self.save()

    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"


class PurchaseItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    purchase = models.ForeignKey(
        Purchase, on_delete=models.CASCADE, related_name="purchase_items")
    expiration_date = models.DateField(null=True, blank=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.quantity} x {self.product.name} comprado en {self.purchase}'

    class Meta:
        verbose_name = "Detalle de compra"
        verbose_name_plural = "Detalles de compra"


class SaleInvoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, null=True, blank=True)
    sale_date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    voided = models.BooleanField(default=False)
    
    def void_sale(self):
        for saleItem in self.sale_invoice_items.all():
            saleItem.product.increment_stock(saleItem.quantity)
        self.voided = True
        self.save()

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"


class SaleInvoiceItem(models.Model):
    sale_invoice = models.ForeignKey(
        SaleInvoice, on_delete=models.CASCADE, related_name="sale_invoice_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Detalle de venta"
        verbose_name_plural = "Detalles de venta"
