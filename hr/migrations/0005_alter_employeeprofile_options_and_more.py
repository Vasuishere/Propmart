# Generated by Django 5.1.7 on 2025-03-27 05:05

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0004_employeeprofile_password'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employeeprofile',
            options={'ordering': ['last_name', 'first_name'], 'verbose_name': 'Employee Profile', 'verbose_name_plural': 'Employee Profiles'},
        ),
        migrations.RemoveField(
            model_name='employeeprofile',
            name='personal_id_number',
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='aadhar_card_number',
            field=models.CharField(blank=True, max_length=12, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Aadhar number must be 12 digits', regex='^\\d{12}$')]),
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='bank_account_number',
            field=models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.RegexValidator(message='Account number must be between 9 and 18 digits', regex='^\\d{9,18}$')]),
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='bank_ifsc_code',
            field=models.CharField(blank=True, max_length=11, null=True, validators=[django.core.validators.RegexValidator(message='Invalid IFSC Code format', regex='^[A-Z]{4}0[A-Z0-9]{6}$')]),
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='bank_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='father_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='gender',
            field=models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='mother_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='pan_card_number',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Invalid PAN Card format', regex='^[A-Z]{5}[0-9]{4}[A-Z]{1}$')]),
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='previous_company_experience_letter',
            field=models.FileField(blank=True, null=True, upload_to='documents/experience_letters/'),
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='previous_company_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='reporting_manager',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subordinates', to='hr.employeeprofile'),
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='uan_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='employeeprofile',
            name='current_address',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='employeeprofile',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hr.department'),
        ),
        migrations.AlterField(
            model_name='employeeprofile',
            name='employee_id',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='employeeprofile',
            name='graduation_degree',
            field=models.FileField(blank=True, null=True, upload_to='documents/degrees/'),
        ),
        migrations.AlterField(
            model_name='employeeprofile',
            name='job_title',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hr.jobtitle'),
        ),
        migrations.AlterField(
            model_name='employeeprofile',
            name='marksheet_10',
            field=models.FileField(blank=True, null=True, upload_to='documents/marksheets/10th/'),
        ),
        migrations.AlterField(
            model_name='employeeprofile',
            name='marksheet_12',
            field=models.FileField(blank=True, null=True, upload_to='documents/marksheets/12th/'),
        ),
        migrations.AlterField(
            model_name='employeeprofile',
            name='password',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='employeeprofile',
            name='permanent_address',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='employeeprofile',
            name='profile_photo',
            field=models.ImageField(blank=True, null=True, upload_to='profile_photos/'),
        ),
        migrations.AlterField(
            model_name='employeeprofile',
            name='salary',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='employeeprofile',
            name='work_location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hr.worklocation'),
        ),
    ]
