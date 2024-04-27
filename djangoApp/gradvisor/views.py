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
from sklearn.impute import SimpleImputer

# Create your views here.
from .forms import ApplicantForm
from .models import Applicant
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

# Get the absolute path to the current directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define the filename for y_train
y_train_filename = 'y_train.csv'

# Construct the full path to y_train.csv
y_train_path = os.path.join(BASE_DIR, y_train_filename)

# Load y_train from the CSV file
y_train = pd.read_csv(y_train_path)

# Check scikit-learn version
if sklearn.__version__ != '1.2.2':
    raise ValueError(f"Expected scikit-learn version 1.2.2, but found {sklearn.__version__}. Please retrain the model.")

try:
    with open(os.path.join(BASE_DIR, 'adaboost_model.pkl'), 'rb') as file:
        ada_model = joblib.load(file)
except ValueError as e:
    print(e)
    print("Please retrain the model.")
    ada_model = None


try:
    with open(os.path.join(BASE_DIR, 'knn_model.pkl'), 'rb') as file:
        knn_model = joblib.load(file)
except ValueError as e:
    print(e)
    print("Please retrain the model.")
    knn_model = None



# Mapping from university name to index
univ_to_index = {
    'Worcester Polytechnic Institute': 53, 'Wayne State University': 52, 'Virginia Polytechnic Institute and State University': 51,
    'University of Wisconsin Madison': 50, 'University of Washington': 49, 'University of Utah': 48, 'University of Texas Dallas': 47,
    'University of Texas Austin': 46, 'University of Texas Arlington': 45, 'University of Southern California': 44, 'University of Pennsylvania': 43,
    'University of North Carolina Charlotte': 42, 'University of North Carolina Chapel Hill': 41, 'University of Minnesota Twin Cities': 40,
    'University of Michigan Ann Arbor': 39, 'University of Massachusetts Amherst': 38, 'University of Maryland College Park': 37,
    'University of Illinois Urbana-Champaign': 36, 'University of Illinois Chicago': 35, 'University of Florida': 34, 'University of Colorado Boulder': 33,
    'University of Cincinnati': 32, 'University of California Santa Cruz': 31, 'University of California Santa Barbara': 30,
    'University of California San Diego': 29, 'University of California Los Angeles': 28, 'University of California Irvine': 27,
    'University of California Davis': 26, 'University of Arizona': 25, 'Texas A and M University College Station': 24, 'Syracuse University': 23,
    'SUNY Stony Brook': 21, 'SUNY Buffalo': 20, 'Stanford University': 22, 'Rutgers University New Brunswick/Piscataway': 19, 'Purdue University': 18,
    'Princeton University': 17, 'Ohio State University Columbus': 16, 'Northwestern University': 15, 'Northeastern University': 14,
    'North Carolina State University': 13, 'New York University': 12, 'New Jersey Institute of Technology': 11, 'Massachusetts Institute of Technology': 10,
    'Johns Hopkins University': 9, 'Harvard University': 8, 'Georgia Institute of Technology': 7, 'George Mason University': 6, 'Cornell University': 5,
    'Columbia University': 4, 'Clemson University': 3, 'Carnegie Mellon University': 2, 'California Institute of Technology': 1, 'Arizona State University': 0
}

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
        'researchExp': [user_data['researchExp']],
        'industryExp': [user_data['industryExp']],
        'internExp': [user_data['internExp']],
        'journalPubs': [user_data['journalPubs']],
        'confPubs': [user_data['confPubs']],
        'cgpa': [user_data['cgpa']],
        'gre_score': [user_data['gre_score']],
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

# Define a function to preprocess the input data
def preprocess_input_data(user_data):
    
    # Create a DataFrame from the user data
    df = pd.DataFrame({
        'researchExp': [user_data['researchExp']],
        'industryExp': [user_data['industryExp']],
        'internExp': [user_data['internExp']],
        'journalPubs': [user_data['journalPubs']],
        'confPubs': [user_data['confPubs']],
        'cgpa': [user_data['cgpa']],
        'gre_score': [user_data['gre_score']],
        'univName': [user_data['univName']],
        'univName_encoded': [user_data['univName_encoded']],  # Include 'univName_encoded'
    })

    # Create an imputer to fill missing values with the mean
    imputer = SimpleImputer(strategy='mean')

    # Fit the imputer on the input data and transform it
    df_imputed = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)

    return df_imputed


def similarity_users(user_data):
    if knn_model is None:
        return None

    # Preprocess the input data to handle NaN values
    df = preprocess_input_data(user_data)

    # Predict the top similar users using the KNN model
    distances, indices = knn_model.kneighbors(df, n_neighbors=3)
        
    # Initialize a set to store unique similar users
    unique_similar_users = set()

    # Iterate over the first 3 similar users
    for distance, idx in zip(distances[0][:5], indices[0][:5]):
        # Calculate similarity (1 - distance)
        similarity = 1 - distance
        # Get the user index and the corresponding target value (user name)
        user_name = y_train.iloc[idx].iloc[0]
        unique_similar_users.add(user_name)
    
    return list(unique_similar_users)


@login_required
def applicant_form(request):
    username = request.user.username
    user_id = request.user.id

    applicant_entry = Applicant.objects.filter(id=user_id).first()

    if request.method == 'POST':
        form = ApplicantForm(request.POST, instance=applicant_entry)
        if form.is_valid():
            # Extract form data
            form.instance.userName = username
            applicant = form.save(commit=False)
            applicant.save()
            researchExp = form.cleaned_data.get('researchExp')
            industryExp = form.cleaned_data.get('industryExp')
            internExp = form.cleaned_data.get('internExp')
            journalPubs = form.cleaned_data.get('journalPubs')
            confPubs = form.cleaned_data.get('confPubs')
            cgpa = form.cleaned_data.get('cgpa')
            gre_score = form.cleaned_data.get('gre_score')

            # Process data into a DataFrame
            user_data = {
                'researchExp': researchExp,
                'industryExp': industryExp,
                'internExp': internExp,
                'journalPubs': journalPubs,
                'confPubs': confPubs,
                'cgpa': cgpa,
                'gre_score': gre_score
            }

            # Make predictions
            top_five_predictions = predict_universities(user_data)
            # Get the top predicted university name
            top_university_name = top_five_predictions[0][0]
           
            # Get the corresponding index from the univ_to_index dictionary
            univ_index = univ_to_index.get(top_university_name)
            
            user_data['univName'] = univ_index
            user_data['univName_encoded'] = univ_index
            similar_users = similarity_users(user_data)

            # Get the top five similar universities
            context = {
                'username': username,
                'cgpa': cgpa,
                'gre_score': gre_score,
                'industryExp': industryExp,
                'researchExp': researchExp,
                'predicted_colleges': top_five_predictions,
                'similarity_users': similar_users,
            }
            return render(request, 'recommendations.html',  context)
    else:
        form = ApplicantForm(instance=applicant_entry) if applicant_entry else ApplicantForm()
    
    return render(request, 'applicant_form.html', {'form': form})

def success(request):
    return render(request, 'success.html')

def applicant_list(request):
    applicants = Applicant.objects.all()
    return render(request, 'applicant_list.html', {'applicants': applicants})


def message_users(request):
    return render(request, 'message_users.html')