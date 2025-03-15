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
from employee import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('vendor-registration/', views.vendor_registration, name='vendor_registration'),
    path('location-registration/<int:vendor_id>/', views.location_registration, name='location_registration'),
    path('contact-registration/<int:location_id>/', views.contact_registration, name='contact_registration'),
    path('purchase_order_view', views.purchase_order_view, name='purchase_order_view'),
    path('about/', views.about, name='about'),
    path('demo/', views.demo, name='demo'),
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('vendor-registration/', views.vendor_registration, name='vendor_registration'),
]