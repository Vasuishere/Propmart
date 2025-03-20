
# Register your models here.
from django.contrib import admin
from .models import VendorRegistration,LocationContact,VendorLocation,PurchaseOrder,PurchaseOrderItem

admin.site.register(LocationContact)
admin.site.register(VendorRegistration)
admin.site.register(VendorLocation)
admin.site.register(PurchaseOrder)
admin.site.register(PurchaseOrderItem)