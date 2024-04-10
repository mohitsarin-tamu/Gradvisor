from django import forms
from .models import Applicant

class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ['GRE_score', 'TOEFL_score', 'university_name', 'GPA']
