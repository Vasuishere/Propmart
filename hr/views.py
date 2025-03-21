from django.shortcuts import render, redirect
from .models import WorkLocation, JobTitle, Department,EmployeeProfile
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

def EmpRegister(request):
    """Handle Employee Registration."""
    if request.method == "POST":
        emp = EmployeeProfile(
            first_name=request.POST.get("first_name"),
            last_name=request.POST.get("last_name"),
            job_title=JobTitle.objects.filter(title=request.POST.get("job_title")).first(),
            department=Department.objects.filter(name=request.POST.get("department")).first(),
            work_location=WorkLocation.objects.filter(city=request.POST.get("work_location")).first(),
            employee_id=generate_employee_id(),
            password = generate_password(),
            contact_email=request.POST.get("contact_email"),
            contact_phone=request.POST.get("contact_phone"),
            joining_date=request.POST.get("joining_date"),
            emergency_contact_name=request.POST.get("emergency_contact_name"),
            emergency_contact_phone=request.POST.get("emergency_contact_phone"),
            current_address=request.POST.get("current_address"),
            permanent_address=request.POST.get("permanent_address"),
            salary=request.POST.get("salary"),
            personal_id_number=request.POST.get("personal_id_number"),
            marksheet_10=request.FILES.get("marksheet_10"),
            marksheet_12=request.FILES.get("marksheet_12"),
            graduation_degree=request.FILES.get("graduation_degree"),
            profile_photo=request.FILES.get("profile_photo"),
        )
        emp.save()
        breakpoint()
        return redirect("hr/Dashboard")

    context = {
        "Work": WorkLocation.objects.values("city"),
        "job": list(JobTitle.objects.values("title", "department__name")),
        "Dep": list(Department.objects.values("name")),
    }
    return render(request, "hr/EmpRegister.html", context)


def Dashboard(request):
    return render(request,"hr/Dashboard.html")

def Demo(request):
    return render(request,"hr/Demo.html")