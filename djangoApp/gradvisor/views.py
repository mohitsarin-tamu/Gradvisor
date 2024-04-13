from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
# Create your views here.
from .forms import ApplicantForm
from .models import Applicant
from django.contrib import messages

def home(request):
    return render(request, 'home.html') 

def signup_login_view(request):
    signup_form = UserCreationForm()
    login_form = AuthenticationForm()

    if request.method == 'POST':
        if 'signup' in request.POST:
            signup_form = UserCreationForm(request.POST)
            if signup_form.is_valid():
                user = signup_form.save()
                login(request, user)
                return redirect('applicant_form')
        elif 'login' in request.POST:
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('applicant_form')

    return render(request, 'signup_login.html', {'signup_form': signup_form, 'login_form': login_form})


def applicant_form(request):
    if request.method == 'POST':
        form = ApplicantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = ApplicantForm()
    
    return render(request, 'applicant_form.html', {'form': form})

def success(request):
    return render(request, 'success.html')

def applicant_list(request):
    applicants = Applicant.objects.all()
    return render(request, 'applicant_list.html', {'applicants': applicants})
