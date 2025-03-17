from django import forms
from .models import VendorRegistration, VendorLocation, LocationContact

# Form for VendorRegistration (Company-level details)
class VendorRegistrationForm(forms.ModelForm):
    class Meta:
        model = VendorRegistration
        fields = ['company_name', 'company_pan_card', 'is_active']  # Removed address, GST, and contact_person

# Form for VendorLocation (Each branch location)
class VendorLocationForm(forms.ModelForm):
    class Meta:
        model = VendorLocation
        fields = ['vendor', 'location_name', 'address', 'company_gst']
    
# Form for LocationContact (Contact details per location)
class LocationContactForm(forms.ModelForm):
    class Meta:
        model = LocationContact
        fields = ['location', 'contact_person', 'phone_number', 'email']
