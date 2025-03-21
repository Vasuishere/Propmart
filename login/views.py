from django.shortcuts import render, redirect
from hr.models import EmployeeProfile
from django.contrib import messages

def employee_login(request):
    if request.method == "POST":
        employee_id = request.POST.get("employee_id")
        password = request.POST["password"]

        try:
            employee = EmployeeProfile.objects.get(employee_id=employee_id, password=password)
            
            if employee.is_active:
                # Get department ID
                department_id = employee.department.id if employee.department else None
                # Map department IDs to dashboard paths
                department_dashboard_mapping = {
                    1: "hr/Dashboard",          # Human Resource
                    2: "IT/Dashboard.html",          # IT
                    3: "Finance/Dashboard.html",     # Finance
                    4: "procurement",       # Sales
                    5: "procurement/index.html",     # Procurement
                    6: "Delivery/login.html"         # Dispatch (Delivery falls under this)
                }

                # Redirect to the respective dashboard
                dashboard_path = department_dashboard_mapping.get(department_id, "general_dashboard")
                return redirect(f"/{dashboard_path}")

            else:
                messages.error(request, "Your account is inactive. Please contact admin.")
        except EmployeeProfile.DoesNotExist:
            messages.error(request, "Invalid Employee ID or Password.")

    return render(request, "login/login.html")


def logout(request):
    return render(request,"/")