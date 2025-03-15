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
    
    def clean(self):
        cleaned_data = super().clean()
        vendor = cleaned_data.get('vendor')
        gst = cleaned_data.get('company_gst')
        
        if not vendor or not gst:
            return cleaned_data
        
        # Check if this is an update
        instance_id = self.instance.id if self.instance else None
        
        # Check if another vendor is using this GST
        others = VendorLocation.objects.filter(company_gst=gst).exclude(vendor=vendor)
        if others.exists():
            vendor_names = set(loc.vendor.company_name for loc in others)
            self.add_error('company_gst', 
                f"This GST number is already used by: {', '.join(vendor_names)}. "
                f"A GST number cannot be shared between different vendors.")
        
        # Check if this vendor already has this GST (for new records)
        if not instance_id:
            if VendorLocation.objects.filter(vendor=vendor, company_gst=gst).exists():
                self.add_error('company_gst', 
                    f"This vendor already has a location with GST number {gst}.")
        
        return cleaned_data

# Form for LocationContact (Contact details per location)
class LocationContactForm(forms.ModelForm):
    class Meta:
        model = LocationContact
        fields = ['location', 'contact_person', 'phone_number', 'email']
