from django import forms
from .models import Applicant

class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ['greQuantitativeScore', 'greVerbalScore', 'greAWAScore', 'GPA', 'toeflScore', 'workExperience', 'underGraduateUniversity']
        help_texts = {
            'greQuantitativeScore': 'out of 170',
            'greVerbalScore': 'out of 170',
            'greAWAScore': 'out of 6.0',
            'GPA': 'in 4-scale',
            'toeflScore': 'out of 120',
            'workExperience': 'in months(internship/fulltime)',
            'underGraduateUniversity': 'Name of the university'
        }