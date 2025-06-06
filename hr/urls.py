"""
URL configuration for propmart project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from login.views import logout
from hr import views 



urlpatterns = [
    path('Dashboard', views.Dashboard, name='Dashboard'),
    path('demo/', views.Demo, name='demo'),
    path('logout/', logout, name='logout'),
    path('EmpDetails/', views.EmpDetails, name='EmpDetails'),
    path('get_job_titles/', views.get_job_titles, name='get_job_titles'),
    path('EmpMoreDetails/<int:Emp_id>/', views.EmpMoreDetails, name='EmpMoreDetails'),
    path('EmpRegister', views.EmpRegister, name='EmpRegister'),
]