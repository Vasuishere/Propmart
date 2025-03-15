from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q, UniqueConstraint

class VendorRegistration(models.Model):
    company_name = models.CharField(
        max_length=200, unique=True, help_text="Name of the company"
    )
    company_pan_card = models.CharField(
        max_length=10, unique=True, help_text="Company PAN Card number (10 characters)"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Date when vendor was registered"
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Date when vendor details were last updated"
    )
    is_active = models.BooleanField(
        default=True, help_text="Indicates if vendor is currently active"
    )

    class Meta:
        verbose_name = "Vendor Registration"
        verbose_name_plural = "Vendor Registrations"
        ordering = ["company_name"]

    def __str__(self):
        return self.company_name


class VendorLocation(models.Model):
    vendor = models.ForeignKey(
        VendorRegistration,
        on_delete=models.CASCADE,
        related_name="locations",
        help_text="Vendor to which this location belongs",
    )
    location_name = models.CharField(
        max_length=200, help_text="Name of the location (e.g., Bangalore, Chennai)"
    )
    address = models.TextField(help_text="Complete location address")
    company_gst = models.CharField(
        max_length=30, help_text="GST number specific to this location (15-30 characters)"
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date when location was added")
    updated_at = models.DateTimeField(auto_now=True, help_text="Date when location details were last updated")
    is_active = models.BooleanField(default=True, help_text="Indicates if location is currently active")

    class Meta:
        verbose_name = "Vendor Location"
        verbose_name_plural = "Vendor Locations"
        ordering = ["location_name"]
        # We'll use a unique_together constraint to ensure no duplicate GST-vendor combinations
        unique_together = [('vendor', 'company_gst')]

    def __str__(self):
        return f"{self.vendor.company_name} - {self.location_name}"

    def clean(self):
        super().clean()
        if not self.company_gst:
            return
            
        # Check if this GST is used by any other vendor - but only if this is a new record
        # or if the GST has changed
        if not self.pk or VendorLocation.objects.get(pk=self.pk).company_gst != self.company_gst:
            others = VendorLocation.objects.filter(
                company_gst=self.company_gst
            ).exclude(vendor=self.vendor)
            
            if others.exists():
                vendor_names = set(loc.vendor.company_name for loc in others)
                raise ValidationError({
                    'company_gst': f"This GST number ({self.company_gst}) is already used by: {', '.join(vendor_names)}. "
                                  f"A GST number cannot be shared between different vendors."
                })
        
        # Check if duplicate GST exists for the same vendor
        if not self.pk:  # Only check for new records
            if VendorLocation.objects.filter(vendor=self.vendor, company_gst=self.company_gst).exists():
                raise ValidationError({
                    'company_gst': f"This vendor already has a location with GST number {self.company_gst}."
                })


class LocationContact(models.Model):
    location = models.ForeignKey(
        VendorLocation,
        on_delete=models.CASCADE,
        related_name="contacts",
        help_text="Location to which this contact belongs",
    )
    contact_person = models.CharField(max_length=100, help_text="Name of the contact person")
    phone_number = models.CharField(
        max_length=15, blank=True, null=True, help_text="Contact phone number"
    )
    email = models.EmailField(blank=True, null=True, help_text="Contact email address")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date when contact was added")
    updated_at = models.DateTimeField(auto_now=True, help_text="Date when contact details were last updated")
    is_active = models.BooleanField(
        default=True, help_text="Indicates if vendor is currently active"
    )

    class Meta:
        verbose_name = "Location Contact"
        verbose_name_plural = "Location Contacts"
        ordering = ["contact_person"]

    def __str__(self):
        return f"Contact for {self.location.vendor.company_name} - {self.location.location_name}"


class PurchaseOrder(models.Model):
    RECEIVE_CHOICES = [
        ('EMAIL', 'Email'),
        ('WHATSAPP', 'WhatsApp'),
        ('OTHER', 'Other'),
    ]
    vendor = models.ForeignKey(VendorRegistration,on_delete=models.CASCADE,related_name='purchase_orders')
    location = models.ForeignKey(VendorLocation,on_delete=models.CASCADE,related_name='orders')
    receive_method = models.CharField(max_length=20,choices=RECEIVE_CHOICES,default='EMAIL')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"PO-{self.id} ({self.vendor.company_name})"

class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(
        PurchaseOrder,
        on_delete=models.CASCADE,
        related_name='items'
    )
    item_name = models.CharField(max_length=200)
    item_details = models.TextField()
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['item_name']

    def __str__(self):
        return f"{self.item_name} (x{self.quantity})"
