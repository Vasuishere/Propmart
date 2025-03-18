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
        fields = ['location_name', 'address', 'company_gst']
        widgets = {
            'location_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter location name'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter address'}),
            'company_gst': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter GST number'}),
        }  # Remove vendor from default fields

    def __init__(self, *args, **kwargs):
        vendor = kwargs.pop('vendor', None)
        super(VendorLocationForm, self).__init__(*args, **kwargs)
        
        if not vendor:
            # Add vendor field only if no vendor is pre-selected
            self.fields['vendor'] = forms.ModelChoiceField(
                queryset=VendorRegistration.objects.all(),
                label="Company"
            )
    
# Form for LocationContact (Contact details per location)
class LocationContactForm(forms.ModelForm):
    class Meta:
        model = LocationContact
        fields = ['contact_person', 'phone_number', 'email']
        # Removed 'location' since it's set in the view
