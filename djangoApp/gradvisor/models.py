from django.db import models

# Create your models here.
class Applicant(models.Model):
    GRE_score = models.IntegerField()
    TOEFL_score = models.IntegerField()
    university_name = models.CharField(max_length=200)
    GPA = models.FloatField()

    class Meta:
        app_label = 'gradvisor'

    def __str__(self):
        return self.university_name