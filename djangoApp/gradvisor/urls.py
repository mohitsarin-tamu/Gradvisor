from django.urls import path
from . import views

urlpatterns = [
    path('', views.applicant_form, name='applicant_form'),
    path('success/', views.success, name='success'),
    path('signup/', views.signup, name='signup'),
]
