# Create your models here.
from django.db import models
from localflavor.in_.models import INStateField
from django.db import models
from django.core.validators import RegexValidator


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
    # Personal Information
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    father_name = models.CharField(max_length=50, null=True, blank=True)
    mother_name = models.CharField(max_length=50, null=True, blank=True)
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    
    contact_email = models.EmailField(unique=True)
    contact_phone = models.CharField(max_length=15)
    
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(max_length=15)
    
    current_address = models.TextField()
    permanent_address = models.TextField()

    # Department Details
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True)
    job_title = models.ForeignKey('JobTitle', on_delete=models.SET_NULL, null=True)
    reporting_manager = models.ForeignKey('EmployeeProfile', on_delete=models.SET_NULL, null=True, related_name='subordinates')
    joining_date = models.DateField()
    work_location = models.ForeignKey('WorkLocation', on_delete=models.SET_NULL, null=True)

    # Previous Employment Details
    previous_company_name = models.CharField(max_length=100, null=True, blank=True)
    previous_company_experience_letter = models.FileField(
        upload_to='documents/experience_letters/', 
        null=True, 
        blank=True
    )
    uan_number = models.CharField(max_length=20, null=True, blank=True)

    # Bank Details
    bank_name = models.CharField(max_length=100, null=True, blank=True)
    bank_account_number = models.CharField(
        max_length=20, 
        null=True,
        blank=True,
        validators=[RegexValidator(
            regex=r'^\d{9,18}$', 
            message='Account number must be between 9 and 18 digits'
        )]
    )
    bank_ifsc_code = models.CharField(
        max_length=11, 
        null=True,
        blank=True,
        validators=[RegexValidator(
            regex=r'^[A-Z]{4}0[A-Z0-9]{6}$', 
            message='Invalid IFSC Code format'
        )]
    )

    # Government Proofs
    aadhar_card_number = models.CharField(
        max_length=12, 
        null=True,  # Make nullable
        blank=True,
        unique=True,
        validators=[RegexValidator(
            regex=r'^\d{12}$', 
            message='Aadhar number must be 12 digits'
        )]
    )
    pan_card_number = models.CharField(
        max_length=10, 
        null=True,  # Make nullable
        blank=True,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$', 
            message='Invalid PAN Card format'
        )]
    )

    # Educational Documents
    marksheet_10 = models.FileField(upload_to="documents/marksheets/10th/", null=True, blank=True)
    marksheet_12 = models.FileField(upload_to="documents/marksheets/12th/", null=True, blank=True)
    graduation_degree = models.FileField(upload_to="documents/degrees/", null=True, blank=True)
    profile_photo = models.ImageField(upload_to="profile_photos/", null=True, blank=True)

    # Additional System Fields
    employee_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    password = models.CharField(max_length=128, null=True, blank=True)  # Use make_password() for hashing
    is_active = models.BooleanField(default=True)
    
    # Optional: Salary and Other Details
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.employee_id or 'No ID'})"

    class Meta:
        verbose_name = 'Employee Profile'
        verbose_name_plural = 'Employee Profiles'
        ordering = ['last_name', 'first_name']
