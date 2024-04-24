from urllib import request
import pandas as pd
import numpy as np # type: ignore
import sklearn
import pickle
import os
import joblib

from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
# Create your views here.
from .forms import ApplicantForm
from .models import Applicant
from django.contrib import messages

# Get the absolute path to the current directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Check scikit-learn version
if sklearn.__version__ != '1.2.2':
    raise ValueError(f"Expected scikit-learn version 1.2.2, but found {sklearn.__version__}. Please retrain the model.")

try:
    with open(os.path.join(BASE_DIR, 'adaboost_model.pkl'), 'rb') as file:
        ada_model = pickle.load(file)
except ValueError as e:
    print(e)
    print("Please retrain the model.")
    ada_model = None

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
                username = signup_form.cleaned_data.get('username')
                login(request, user)
                print(f"User {username} signed up successfully!")
                return redirect('applicant_form')
            else:
                print("Signup form errors:", signup_form.errors)

        elif 'login' in request.POST:
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('applicant_form')
                else:
                    print("Authentication failed")

    return render(request, 'signup_login.html', {'signup_form': signup_form, 'login_form': login_form})


def predict_universities(user_data):
    
    if ada_model is None:
        return None

     # Create a DataFrame from the user data
    df = pd.DataFrame({
        'greQuantitativeScore': [user_data['greQuantitativeScore']],
        'greVerbalScore': [user_data['greVerbalScore']],
        'greAWAScore': [user_data['greAWAScore']],
        'GPA': [user_data['GPA']],
        'workExperience': [user_data['workExperience']],
        'researchExperience': [user_data['researchExperience']]
    })
    
    # Make predictions
    predictions = ada_model.predict_proba(df)

    # Get the classes
    classes = ada_model.classes_
    
    # Initialize a list to store top five precision predictions
    top_five_predictions = []
    
    # Get the indices of the top five classes with the highest probabilities
    top_five_indices = np.argsort(predictions)[0][-5:][::-1]
    
    # Get the corresponding classes and probabilities
    top_five_classes = classes[top_five_indices]
    top_five_probs = predictions[0][top_five_indices]
    
    # Store the top five precision predictions
    top_five_predictions = list(zip(top_five_classes, top_five_probs))

    return top_five_predictions


def applicant_form(request):
    if request.method == 'POST':
        form = ApplicantForm(request.POST)
        if form.is_valid():
            # Extract form data
            greQuantitativeScore = form.cleaned_data.get('greQuantitativeScore')
            greVerbalScore = form.cleaned_data.get('greVerbalScore')
            greAWAScore = form.cleaned_data.get('greAWAScore')
            GPA = form.cleaned_data.get('GPA')
            toeflScore = form.cleaned_data.get('toeflScore')
            workExperience = form.cleaned_data.get('workExperience')
            researchExperience = form.cleaned_data.get('researchExperience')

            # Process data into a DataFrame
            user_data = {
                'greQuantitativeScore': greQuantitativeScore,
                'greVerbalScore': greVerbalScore,
                'greAWAScore': greAWAScore,
                'GPA': GPA,
                'toeflScore': toeflScore,
                'workExperience': workExperience,
                'researchExperience': researchExperience
            }

            # Make predictions
            top_five_predictions = predict_universities(user_data)
            
            return render(request, 'recommendations.html', {'top_five_predictions': top_five_predictions})
    else:
        form = ApplicantForm()
    
    return render(request, 'applicant_form.html', {'form': form})

def success(request):
    return render(request, 'success.html')

def applicant_list(request):
    applicants = Applicant.objects.all()
    return render(request, 'applicant_list.html', {'applicants': applicants})
