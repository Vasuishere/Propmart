from django.shortcuts import render, redirect,get_object_or_404
from .forms import VendorRegistrationForm,VendorLocationForm,LocationContactForm,EmployeeForm
from .models import VendorRegistration,VendorLocation,LocationContact


def vendor_registration(request):
    if request.method == 'POST':
        vendor_form = VendorRegistrationForm(request.POST)
        if vendor_form.is_valid():
            vendor = vendor_form.save()
            return redirect('procurement:location_registration', vendor.id)  # Corrected redirect

    else:
        vendor_form = VendorRegistrationForm()

    return render(request, 'procurement/vendor_registration.html', {'vendor_form': vendor_form})

# STEP 2: Location Registration
def location_registration(request, cmp_id):
    vendor = get_object_or_404(VendorRegistration, id=cmp_id)

    if request.method == 'POST':
        cmpGst = request.POST['company_gst']
        vendorModel = VendorLocation.objects
        vendorData = vendorModel.filter(company_gst = cmpGst).values('id')
        location_form = VendorLocationForm(request.POST, vendor=vendor)
        if [item for item in vendorData if item['id'] == cmp_id] and location_form.is_valid():
            location = location_form.save(commit=False)
            location.vendor = vendor  # Always set the vendor from the URL
            location.save()
            insertedLocationId = vendorModel.filter(vendor_id=cmp_id).values('id').order_by('-id').first()
            return redirect('procurement:contact_registration', insertedLocationId['id'])  # Corrected redirect

    else:
        location_form = VendorLocationForm(vendor=vendor)

    return render(request, 'procurement/location_registration.html', {
        'location_form': location_form,
        'vendor': vendor,
        'errorMsg':'GST No. already linked with another company!'
    })

# STEP 3: Contact Registration
def contact_registration(request, location_id):
    location = get_object_or_404(VendorLocation, id=location_id)

    if request.method == 'POST':
        contact_form = LocationContactForm(request.POST)
        if contact_form.is_valid():
            contact = contact_form.save(commit=False)
            contact.location = location  # Link contact to selected location
            contact.save()
            return redirect('procurement:company/')  # Corrected redirect

    else:
        contact_form = LocationContactForm()

    return render(request, 'procurement/contact_registration.html', {
        'contact_form': contact_form,
        'location': location
    })


def index(request):
    return render(request, 'procurement/index.html')

def company(request):
    cmp = VendorRegistration.objects.all()
    context = {
        'cmp': cmp,
    }
    return render(request, 'procurement/company.html', context)

def company_details(request, cmp_id):
    """
    View function to display vendor/company details
    """
    vendor = get_object_or_404(VendorRegistration, id=cmp_id)
    locations = VendorLocation.objects.filter(vendor=vendor)
    
    # Check if a location is selected
    location_id = request.GET.get('location_id')
    selected_location = None
    contacts = None
    
    if location_id:
        selected_location = get_object_or_404(VendorLocation, id=location_id, vendor=vendor)
        contacts = LocationContact.objects.filter(location=selected_location)
    
    context = {
        'vendor': vendor,
        'locations': locations,
        'selected_location': selected_location,
        'contacts': contacts,
    }
    return render(request, 'procurement/company_details.html', context)

def contact(request):
    return render(request, 'procurement/contact.html')

# views.py
def purchase_order_view(request):
    # Get all active companies for the initial dropdown
    companies = VendorRegistration.objects.filter(is_active=True)
    
    # Initialize variables
    locations = None
    contacts = None
    selected_company = None
    selected_location = None
    gst_list = None
    
    # Get selected company ID from request
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
                try:
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
                    # Split GST numbers if they exist
                    if selected_location.company_gst:
                        gst_list = selected_location.company_gst.split(',')
                    else:
                        gst_list = []
                except VendorLocation.DoesNotExist:
                    # Handle case where location doesn't exist
                    selected_location = None
                    
        except VendorRegistration.DoesNotExist:
            # Handle case where company doesn't exist
            selected_company = None
            locations = None

    context = {
        'companies': companies,
        'locations': locations,
        'contacts': contacts,
        'selected_company': selected_company,
        'selected_location': selected_location,
        'gst_list': gst_list,
    }
    
    return render(request, 'procurement/purchaseorder.html', context)

def demo(request):
    return render(request,'procurement/demo.html')


def register_employee(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('procurement:success_page')  # Change to your success URL
    else:
        form = EmployeeForm()

    return render(request, 'procurement/employee_registration.html', {'form': form})