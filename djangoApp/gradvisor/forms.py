from django import forms
from .models import Applicant

class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ['greQuantitativeScore', 'greVerbalScore', 'greAWAScore', 'GPA', 'toeflScore', 'workExperience', 'underGraduateUniversity', 'researchExperience']
        help_texts = {
            'greQuantitativeScore': 'out of 170',
            'greVerbalScore': 'out of 170',
            'greAWAScore': 'out of 6.0',
            'GPA': 'scale of 4.0',
            'toeflScore': 'out of 120',
            'workExperience': 'in months(internship/fulltime)',
            'researchExperience': 'in months',
        }
        labels = {
            'greQuantitativeScore': 'GRE Quant Score',
            'greVerbalScore': 'GRE Verbal Score',
            'greAWAScore': 'GRE AWA Score',
            'GPA': 'GPA',
            'toeflScore': 'TOEFL Score',
            'workExperience': 'Work Experience',
            'underGraduateUniversity': 'Undergraduate University',
            'researchExperience': 'Research Experience',
        }
