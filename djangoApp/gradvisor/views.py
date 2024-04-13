from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
# Create your views here.
from .forms import ApplicantForm
from .models import Applicant

def home(request):
    return render(request, 'home.html') 

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

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                print(f"User {username} signed up successfully!")
                return redirect('applicant_form') 
            else:
                print("Authentication failed")
        else:
            print(form.errors)
    else:
        form = UserCreationForm()
    
    return render(request, 'signup.html', {'form': form})