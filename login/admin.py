from django.contrib import admin
from .models import EmployeeProfile,Department,WorkLocation,JobTitle


admin.site.register(EmployeeProfile)
admin.site.register(Department)
admin.site.register(WorkLocation)
admin.site.register(JobTitle)