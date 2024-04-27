from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include

# urlpatterns = [
#     path('applicant_form', views.applicant_form, name='applicant_form'),
#     path('success/', views.success, name='success'),
#     path('admin/', admin.site.urls),
#     path('', views.home, name='home'),
#     path('signup_login/', views.signup_login_view, name='signup_login'),
# ]
urlpatterns = [
    path('', views.home, name='home'),
    path('signup_login/', views.signup_login_view, name='signup_login'),
    path('applicant_form/', views.applicant_form, name='applicant_form'),
    path('success/', views.success, name='success'),
    path('recommendations/', views.applicant_form, name='recommendations'),
    path('message_users/', views.message_users, name='message_users'),
    path('admin/', admin.site.urls),
]