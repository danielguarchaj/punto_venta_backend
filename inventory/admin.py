from django.contrib import admin

from inventory.models import Brand, Category, Product, Purchase, PurchaseItem

admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Purchase)
admin.site.register(PurchaseItem)