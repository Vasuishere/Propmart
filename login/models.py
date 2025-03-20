from django.db import models
from django.contrib.auth.models import User
from localflavor.in_.models import INStateField

class WorkLocation(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = INStateField()
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class JobTitle(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="job_titles")
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.title} ({self.department.name})"

class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    job_title = models.ForeignKey(JobTitle, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    work_location = models.ForeignKey(WorkLocation, on_delete=models.SET_NULL, null=True)

    employee_id = models.CharField(max_length=50, unique=True)
    contact_email = models.EmailField(unique=True)
    contact_phone = models.CharField(max_length=15)
    joining_date = models.DateField()
    
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(max_length=15)
    current_address = models.CharField(max_length=100)
    permanent_address = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    personal_id_number = models.CharField(max_length=50)

    # File Uploads
    marksheet_10 = models.FileField(upload_to="documents/marksheets/10th/")
    marksheet_12 = models.FileField(upload_to="documents/marksheets/12th/")
    graduation_degree = models.FileField(upload_to="documents/degrees/")
    profile_photo = models.ImageField(upload_to="profile_photos/")

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
