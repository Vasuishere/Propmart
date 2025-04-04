from django.shortcuts import render, redirect
from .models import WorkLocation, JobTitle, Department,EmployeeProfile
from django.db import transaction
from django.contrib import messages
from django.http import JsonResponse

import string
import random

def generate_employee_id(length=8):
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return ''.join(random.choices(chars, k=length))

def generate_password(length=10):
    special_chars = "!@#$"
    all_chars = string.ascii_uppercase + string.ascii_lowercase + string.digits + special_chars
    
    password = [
        random.choice(string.ascii_uppercase),
        random.choice(string.ascii_lowercase),
        random.choice(string.digits),
        random.choice(special_chars),
    ]
    password += random.choices(all_chars, k=length - 4)
    random.shuffle(password)
    
    return ''.join(password)

def get_job_titles(request):
    department_name = request.GET.get('department')
    if department_name:
        try:
            department = Department.objects.get(name=department_name)
            job_titles = list(JobTitle.objects.filter(department=department).values_list('title', flat=True))
            return JsonResponse({'job_titles': job_titles})
        except Department.DoesNotExist:
            return JsonResponse({'job_titles': []})
    return JsonResponse({'job_titles': []})


def EmpRegister(request):
    """Handle Employee Registration with dynamic job title filtering."""
    if request.method == "POST":
        try:
            # Get foreign key objects
            department = Department.objects.filter(name=request.POST.get("department")).first()
            if not department:
                raise ValueError("Invalid department selected")
                
            job_title = JobTitle.objects.filter(
                title=request.POST.get("job_title"), 
                department=department
            ).first()
            if not job_title:
                raise ValueError("Invalid job title selected")
                
            work_location = WorkLocation.objects.filter(city=request.POST.get("work_location")).first()
            if not work_location:
                raise ValueError("Invalid work location selected")

            # Validate required fields
            required_fields = ['first_name', 'last_name', 'contact_email', 'contact_phone', 
                             'joining_date', 'bank_name', 'bank_account_number', 'bank_ifsc_code']
            for field in required_fields:
                if not request.POST.get(field):
                    raise ValueError(f"{field.replace('_', ' ').title()} is required")

            # Validate file uploads
            required_files = ['marksheet_10', 'marksheet_12', 'graduation_degree', 'profile_photo']
            for file_field in required_files:
                if not request.FILES.get(file_field):
                    raise ValueError(f"{file_field.replace('_', ' ').title()} is required")

            # Use transaction to ensure data integrity
            with transaction.atomic():
                emp = EmployeeProfile(
                    # Personal Information
                    first_name=request.POST.get("first_name"),
                    last_name=request.POST.get("last_name"),
                    father_name=request.POST.get("father_name"),
                    mother_name=request.POST.get("mother_name"),
                    gender=request.POST.get("gender"),
                    
                    # Contact Information
                    contact_email=request.POST.get("contact_email"),
                    contact_phone=request.POST.get("contact_phone"),
                    emergency_contact_name=request.POST.get("emergency_contact_name"),
                    emergency_contact_phone=request.POST.get("emergency_contact_phone"),
                    
                    # Addresses
                    current_address=request.POST.get("current_address"),
                    permanent_address=request.POST.get("permanent_address"),
                    
                    # Department Details
                    department=department,
                    job_title=job_title,
                    work_location=work_location,
                    joining_date=request.POST.get("joining_date"),
                    
                    # Previous Employment
                    previous_company_name=request.POST.get("previous_company_name"),
                    uan_number=request.POST.get("uan_number"),
                    
                    # Bank Details
                    bank_name=request.POST.get("bank_name"),
                    bank_account_number=request.POST.get("bank_account_number"),
                    bank_ifsc_code=request.POST.get("bank_ifsc_code"),
                    
                    # Government Proofs
                    aadhar_card_number=request.POST.get("aadhar_card_number"),
                    pan_card_number=request.POST.get("pan_card_number"),
                    
                    # Document Uploads
                    marksheet_10=request.FILES.get("marksheet_10"),
                    marksheet_12=request.FILES.get("marksheet_12"),
                    graduation_degree=request.FILES.get("graduation_degree"),
                    previous_company_experience_letter=request.FILES.get("previous_company_experience_letter"),
                    profile_photo=request.FILES.get("profile_photo"),
                    
                    # System Fields
                    employee_id=generate_employee_id(),
                    password=generate_password(),
                    
                    # Optional Fields
                    salary=request.POST.get("salary") if request.POST.get("salary") else None
                )
                emp.save()
                
                messages.success(request, 
                    f"Employee {emp.first_name} {emp.last_name} registered successfully! "
                    f"Employee ID: {emp.employee_id}"
                )
                return redirect("Dashboard")
        
        except ValueError as e:
            messages.error(request, str(e))
            return redirect("EmpRegister")
        except Exception as e:
            messages.error(request, f"Registration failed: {str(e)}")
            return redirect("EmpRegister")

    # GET request handling
    context = {
        "departments": Department.objects.all(),
        "work_locations": WorkLocation.objects.all(),
    }
    return render(request, "hr/EmpRegister.html", context)


def Dashboard(request):
    return render(request,"hr/Dashboard.html")

def EmpDetails(request):
    Emp = EmployeeProfile.objects.all()
    context = {
        "Emp" : Emp
    }
    return render(request,"hr/EmpDetails.html",context)

def EmpMoreDetails(request, Emp_id):
    employee = EmployeeProfile.objects.get(pk=Emp_id)
    context = {
        "employee" : employee
    }
    return render(request,"hr/EmpMoreDetails.html", context)

def Demo(request):
    return render(request,"hr/demo.html")