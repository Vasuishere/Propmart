# Generated by Django 5.1.7 on 2025-03-20 16:50

import django.db.models.deletion
import localflavor.in_.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('login', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='WorkLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('address', models.TextField()),
                ('city', models.CharField(max_length=100)),
                ('state', localflavor.in_.models.INStateField(max_length=2)),
                ('country', models.CharField(max_length=100)),
                ('postal_code', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='JobTitle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_titles', to='login.department')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('employee_id', models.CharField(max_length=50, unique=True)),
                ('contact_email', models.EmailField(max_length=254, unique=True)),
                ('contact_phone', models.CharField(max_length=15)),
                ('joining_date', models.DateField()),
                ('emergency_contact_name', models.CharField(max_length=100)),
                ('emergency_contact_phone', models.CharField(max_length=15)),
                ('salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('personal_id_number', models.CharField(max_length=50)),
                ('marksheet_10', models.FileField(upload_to='documents/marksheets/10th/')),
                ('marksheet_12', models.FileField(upload_to='documents/marksheets/12th/')),
                ('graduation_degree', models.FileField(upload_to='documents/degrees/')),
                ('profile_photo', models.ImageField(upload_to='profile_photos/')),
                ('is_active', models.BooleanField(default=True)),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='login.department')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('job_title', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='login.jobtitle')),
                ('work_location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='login.worklocation')),
            ],
        ),
    ]
