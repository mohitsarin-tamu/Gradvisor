from django import forms
from .models import Applicant

class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = [
            'researchExp',
            'industryExp',
            'internExp',
            'journalPubs',
            'confPubs',
            'cgpa',
            'gre_score'
        ]
        help_texts = {
            'internExp': 'in months',
            'researchExp': 'in months',
            'industryExp': 'in months',
            'journalPubs': 'Number of journal publications',
            'confPubs': 'Number of conference publications',
            'cgpa': 'scale of 4.0',
            'gre_score': 'out of 340',
        }
        labels = {
            'researchExp': 'Research Experience',
            'industryExp': 'Industry Experience',
            'internExp': 'Internship Experience',
            'journalPubs': 'Journal Publications',
            'confPubs': 'Conference Publications',
            'cgpa': 'CGPA',
            'gre_score': 'GRE Score'
        }
