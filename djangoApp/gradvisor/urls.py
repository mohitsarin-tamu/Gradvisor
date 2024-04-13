from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', views.applicant_form, name='applicant_form'),
    path('success/', views.success, name='success'),
    # path('login/', views.login_view, name='login'),
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
]