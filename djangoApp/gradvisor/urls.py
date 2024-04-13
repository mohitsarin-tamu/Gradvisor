from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('applicant_form/', views.applicant_form, name='applicant_form'),
    # path('success/', views.success, name='success'),
    # path('login/', views.login_view, name='login'),
    path('admin/', admin.site.urls),
    path('', views.signup_login_view, name='login_signup'),
]