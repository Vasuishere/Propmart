from django.shortcuts import render, redirect
from hr.models import EmployeeProfile
from django.contrib import messages

# Department Dashboard Mapping
DEPARTMENT_DASHBOARD_MAPPING = {
    1: "hr/Dashboard",          # Human Resource
    2: "IT/Dashboard.html",      # IT
    3: "Finance/Dashboard.html", # Finance
    4: "sales/dashboard.html",   # Sales
    5: "procurement/index.html", # Procurement
    6: "procurement",
    7: "general_dashboard",
}

def employee_login(request):
    emp_session = request.session.get("employe_login", {})

    # If session exists, retrieve department_id and redirect
    if emp_session.get("emp_login"):
        department_id = emp_session.get("dep_id", None)
        dashboard_path = DEPARTMENT_DASHBOARD_MAPPING.get(department_id, "general_dashboard")
        return redirect(f"/{dashboard_path}")

    if request.method == "POST":
        employee_id = request.POST.get("employee_id")
        password = request.POST.get("password")  # Use .get() to avoid KeyError

        try:
            employee = EmployeeProfile.objects.get(employee_id=employee_id, password=password)
            if employee.is_active:
                department_id = employee.department.id if employee.department else None

                # Store employee session data in the browser
                request.session["employe_login"] = {
                    "emp_login": True,
                    "emp_id": employee_id,
                    "dep_id": department_id
                }

                # Redirect based on department
                dashboard_path = DEPARTMENT_DASHBOARD_MAPPING.get(department_id, "general_dashboard")
                return redirect(f"/{dashboard_path}")

            else:
                messages.error(request, "Your account is inactive. Please contact admin.")
        except EmployeeProfile.DoesNotExist:
            messages.error(request, "Invalid Employee ID or Password.")

    return render(request, "login/login.html")




def logout(request):
    if 'employe_login' in request.session:
        del request.session['employe_login']  # Remove session key

    return redirect('http://127.0.0.1:8000')  # Redirect to homepage
