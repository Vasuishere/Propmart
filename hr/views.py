from django.shortcuts import render, redirect
from .models import WorkLocation, JobTitle, Department,EmployeeProfile
from django.http import JsonResponse
from .models import JobTitle


def EmpRegister(request):
    Work = WorkLocation.objects.all().values('city')
    job = JobTitle.objects.all().values('title', 'department__name')
    Dep = Department.objects.all().values('name')

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        job_title = request.POST.get("job_title")
        department = request.POST.get("department")
        work_location = request.POST.get("work_location")
        employee_id = request.POST.get("employee_id")
        contact_email = request.POST.get("contact_email")
        contact_phone = request.POST.get("contact_phone")
        joining_date = request.POST.get("joining_date")
        emergency_contact_name = request.POST.get("emergency_contact_name")
        emergency_contact_phone = request.POST.get("emergency_contact_phone")
        current_address = request.POST.get("current_address")
        permanent_address = request.POST.get("permanent_address")
        salary = request.POST.get("salary")
        personal_id_number = request.POST.get("personal_id_number")
        # File uploads
        marksheet_10 = request.FILES.get("marksheet_10")
        marksheet_12 = request.FILES.get("marksheet_12")
        graduation_degree = request.FILES.get("graduation_degree")
        profile_photo = request.FILES.get("profile_photo")

        # Get ForeignKey objects
        job_title_obj = JobTitle.objects.filter(title=job_title).first()
        department_obj = Department.objects.filter(name=department).first()
        work_location_obj = WorkLocation.objects.filter(city=work_location).first()

        # Save data in the model
        emp = EmployeeProfile(
            first_name=first_name,
            last_name=last_name,
            job_title=job_title_obj,
            department=department_obj,
            work_location=work_location_obj,
            employee_id=employee_id,
            contact_email=contact_email,
            contact_phone=contact_phone,
            joining_date=joining_date,
            emergency_contact_name=emergency_contact_name,
            emergency_contact_phone=emergency_contact_phone,
            current_address=current_address,
            permanent_address=permanent_address,
            salary=salary,
            personal_id_number=personal_id_number,
            marksheet_10=marksheet_10,
            marksheet_12=marksheet_12,
            graduation_degree=graduation_degree,
            profile_photo=profile_photo
        )
        breakpoint()
        emp.save()
        return redirect("dashboard")  # Redirect to dashboard after successful registration

    context = {
        "Work": Work,
        "job": list(job),
        "Dep": list(Dep),
    }
    return render(request, "hr/EmpRegister.html", context)




def Dashboard(request):
    return render(request,"hr/Dashboard.html")