from django.db import models

# Create your models here.
class Applicant(models.Model):
    username = models.CharField(max_length=100, default=False)
    passwordVal = models.CharField(max_length=100, default=False)
    researchExp = models.IntegerField(default=0)
    industryExp = models.IntegerField(default=0)
    internExp = models.FloatField(default=0.0)
    journalPubs = models.IntegerField(default=0)
    confPubs = models.IntegerField(default=0)
    cgpa = models.FloatField(default=0)
    gre_score = models.IntegerField(default=260)

    class Meta:
        app_label = 'gradvisor'

    def __str__(self):
        return self.university_name