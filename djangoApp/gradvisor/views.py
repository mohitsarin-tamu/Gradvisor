from django.shortcuts import render, redirect
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