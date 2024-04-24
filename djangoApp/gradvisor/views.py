from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User 
import joblib
import pandas as pd
import os
import numpy as np

# Create your views here.
from .forms import ApplicantForm
from .models import Applicant
from django.contrib import messages
from django.urls import reverse


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


# def applicant_form(request):
#     if request.method == 'POST':
#         form = ApplicantForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('success')
#     else:
#         form = ApplicantForm()
    
#     return render(request, 'applicant_form.html', {'form': form})

def applicant_form(request):
    if request.method == 'POST':
        form = ApplicantForm(request.POST)
        if form.is_valid():
            # Save form data to the database
            applicant_instance = form.save(commit=False)
            username = request.user.username
            applicant_instance.userName = username
            applicant_instance.save()

            # Extract data submitted by the applicant
            applicant_data = {
                #'userName':  applicant_instance.userName,
                #'major': 'Computer Science',
                #'researchExp':1,
                #'industryExp':1,
                #'internExp':1,	
                #'greV':	applicant_instance.greVerbalScore,
                #'greQ':	applicant_instance.greQuantitativeScore,
                #'journalPubs': 1,	
                #'confPubs':	1,
                #'cgpa':	applicant_instance.GPA,
                #'univName':	applicant_instance.underGraduateUniversity,
                #'admit': 0,
                'researchExp': 1, 
                'industryExp': 1, 
                'internExp': 1, 
                'journalPubs': 1, 
                'confPubs': 1,
                'cgpa': 4, 
                'grescore': 300, 
                'major_Aerospace Engineering':0,
                'major_Automotive Engineering':0, 
                'major_Biomedical Engineering':0,
                'major_Chemical Engineering':0, 
                'major_Civil Engineering': 0,
                'major_Computer Science': 1, 
                'major_Computer Science and Engineering':1,
                'major_Data Science':0, 
                'major_Earth and Planetary Sciences':0, 
                'major_Electrical and Computer Engineering':0,
                'major_Electronics and Communication':0,
                'major_Electronics and Communication Engineering':0,
                'major_Engineering Management':0, 
                'major_Finance':0,
                'major_Geographic and Cartographic Sciences':0,
                'major_Industrial Engineering':0, 
                'major_MBA':0, 
                'major_MIS':0,
                'major_Mass Communication':0, 
                'major_Materials Science & Engineering':0,
                'major_Mathematics':0, 
                'major_Mechanical Engineering':0,
                'major_Nanoscale Engineering':0, 
                'major_Naval architecture':0,
                'major_Nuclear Engineering':0, 
                'major_Other':0, 
                'major_Pharmaceutics':0,
                'major_Psychology':0, 
                'major_Public Health & Social work':0,
                'major_Renewable energy':0, 
                'major_Robotics':0,
                'major_Sustainable Energy Technology':0,
                'major_Veterinary & Animal Science':0,
                'major_apparels and fashion technology':0, 
                'major_economics':0,
                'major_environmental engineering':0, 
                'major_oral biology':0,
                'major_petroleum engineering':0, 
                'major_pharmaceutics':0, 
                'major_physics':0,
                'major_renewable energy':0
                # Add other fields as necessary
            }

            # Reshape the data to match the input shape required by the model
            test_data = pd.DataFrame([applicant_data])

            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

            # Construct the relative path to the pickle file
            relative_path_to_pickle = os.path.join(base_dir, 'algorithm_model', 'random_forest_model_checkpoint.pkl')
        
            # Check if the file exists
            if os.path.exists(relative_path_to_pickle):
                # Load the saved model
                loaded_model = joblib.load(relative_path_to_pickle)
            else:
                # Handle the case where the file does not exist
                print("Pickle file does not exist!")

            # Predict the university for the input test data
            # predicted_university = loaded_model.predict(test_data)
            predicted_proba = loaded_model.predict_proba(test_data)
            top_five_indices = np.argsort(predicted_proba[0])[::-1][:5]
            top_five_colleges = loaded_model.classes_[top_five_indices]
            print("Predicted University:", top_five_colleges)
            predicted_colleges = '\n'.join([f"{index + 1}. {college}" for index, college in enumerate(top_five_colleges)])
            # For example:
            applicant_instance.prediction_result = top_five_colleges
            applicant_instance.save()

            # return redirect('success')
            # Pass applicant details to the template
            context = {
                'username': applicant_instance.userName,
                'cgpa': applicant_instance.GPA,
                'gre_scores': f"Verbal: {applicant_instance.greVerbalScore}, Quantitative: {applicant_instance.greQuantitativeScore}",
                'predicted_colleges': predicted_colleges,
            }

            # Render the template with applicant details
            return render(request, 'applicant_details.html', context)
    else:
        form = ApplicantForm()
    
    return render(request, 'applicant_form.html', {'form': form})

def success(request):
    return render(request, 'success.html')

def applicant_list(request):
    applicants = Applicant.objects.all()
    return render(request, 'applicant_list.html', {'applicants': applicants})
