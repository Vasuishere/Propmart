from django.db import models


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
        max_length=15, unique=True, help_text="GST number specific to this location (15 characters)"
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date when location was added")
    updated_at = models.DateTimeField(auto_now=True, help_text="Date when location details were last updated")
    is_active = models.BooleanField(default=True, help_text="Indicates if location is currently active")

    class Meta:
        verbose_name = "Vendor Location"
        verbose_name_plural = "Vendor Locations"
        ordering = ["location_name"]

    def __str__(self):
        return f"{self.vendor.company_name} - {self.location_name}"


class LocationContact(models.Model):
    location = models.ForeignKey(
        VendorLocation,
        on_delete=models.CASCADE,
        related_name="contacts",
        help_text="Location to which this contact belongs",
    )
    contact_person = models.CharField(max_length=100, help_text="Name of the contact person")
    Position = models.CharField(max_length=30, help_text="Job Profile Name (e.g: HPD , PDH)")
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
        return f"Contact for {self.location.vendor.company_name} - {self.location.location_name} - {self.contact_person}"


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
    
    




class Employee(models.Model):
    full_name = models.CharField(max_length=100, help_text="Enter You Name")
    job_title = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=50, unique=True)
    contact_email = models.EmailField(unique=True)
    contact_phone = models.CharField(max_length=15)
    start_date = models.DateField()
    work_location = models.CharField(max_length=255)
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(max_length=15)
    Manager = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    bank_account = models.CharField(max_length=50)
    personal_id = models.CharField(max_length=50, unique=True)  # SSN, Aadhaar, etc.
    education = models.CharField(max_length=255)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    def __str__(self):
        return self.full_name


