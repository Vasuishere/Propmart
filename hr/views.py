from django.shortcuts import render
from login.models import WorkLocation,EmployeeProfile,JobTitle,Department

# Create your views here.


def EmpRegister(request):
    Work = WorkLocation.objects.all().values('city')
    job = JobTitle.objects.all().values('title', 'department__name')  # Include department name
    Dep = Department.objects.all().values('name')
    
    context = {
        "Work": Work,
        "job": list(job),  # Convert queryset to list for JavaScript
        "Dep": list(Dep),
    }
    return render(request, "hr/EmpRegister.html", context)

def Dashboard(request):
    return render(request,"hr/Dashboard.html")