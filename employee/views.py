# views.py
from django.shortcuts import render, redirect
from .forms import VendorRegistrationForm,VendorLocationForm,LocationContactForm
from .models import VendorRegistration,VendorLocation,LocationContact
from django.contrib import messages
from .models import PurchaseOrder, PurchaseOrderItem# If renamed


def vendor_registration(request):
    if request.method == 'POST':
        vendor_form = VendorRegistrationForm(request.POST)
        location_form = VendorLocationForm(request.POST)
        contact_form = LocationContactForm(request.POST)

        if vendor_form.is_valid() and location_form.is_valid() and contact_form.is_valid():
            vendor = vendor_form.save()  # Save vendor first
            location = location_form.save(commit=False)  # Don't save yet
            location.vendor = vendor  # Link location to vendor
            location.save()  # Save location
            
            contact = contact_form.save(commit=False)  # Don't save yet
            contact.location = location  # Link contact to location
            contact.save()  # Save contact

            return redirect('success_url')  # Replace with your actual success page

    else:
        vendor_form = VendorRegistrationForm()
        location_form = VendorLocationForm()
        contact_form = LocationContactForm()

    return render(request, 'vendor_registration.html', {
        'vendor_form': vendor_form,
        'location_form': location_form,
        'contact_form': contact_form
    })

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

# views.py
def purchase_order_view(request):
    # Get all active companies for the initial dropdown
    companies = VendorRegistration.objects.filter(is_active=True)
    
    # Initialize variables
    locations = None
    contacts = None
    selected_company = None
    selected_location = None
    
    # Get selected company ID from request (could be from GET or POST)
    company_id = request.GET.get('company_id')
    
    if company_id:
        try:
            # Get the selected company
            selected_company = VendorRegistration.objects.get(
                id=company_id, 
                is_active=True
            )
            # Filter locations for selected company only
            locations = VendorLocation.objects.filter(
                vendor=selected_company,
                is_active=True
            )
            
            # Get selected location if provided
            location_id = request.GET.get('location_id')
            if location_id:
                selected_location = VendorLocation.objects.get(
                    id=location_id,
                    vendor=selected_company,
                    is_active=True
                )
                # Get contacts for selected location
                contacts = LocationContact.objects.filter(
                    location=selected_location,
                    is_active=True
                )
                
        except VendorRegistration.DoesNotExist:
            # Handle case where company doesn't exist
            pass
        except VendorLocation.DoesNotExist:
            # Handle case where location doesn't exist
            pass

    return render(request, 'purchaseorder.html', {
        'companies': companies,
        'locations': locations,
        'contacts': contacts,
        'selected_company': selected_company,
        'selected_location': selected_location,
    })