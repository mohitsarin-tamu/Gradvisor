"""
URL configuration for gradvisorWebSite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from gradvisor.views import home, applicant_list

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', home, name='home'),
    path('applicant/', include('gradvisor.urls')),
    path('applicant_list/', applicant_list, name='applicant_list'),
]
