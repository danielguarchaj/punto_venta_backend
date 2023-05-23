from django.contrib import admin

from inventory.models import (
    Brand,
    Category,
    Product,
    Purchase,
    PurchaseItem,
    SaleInvoice,
    SaleInvoiceItem,
    Provider,
)

admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Purchase)
admin.site.register(PurchaseItem)
admin.site.register(SaleInvoice)
admin.site.register(SaleInvoiceItem)
admin.site.register(Provider)
