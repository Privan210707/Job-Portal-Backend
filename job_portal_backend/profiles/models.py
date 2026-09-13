from django.conf import settings
from django.db import models

# Create your models here.
class CandidateProfile(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='candidate_profile')
    phone=models.CharField(max_length=20,blank=True)
    bio=models.TextField(blank=True)
    location=models.CharField(max_length=100,blank=True)
    skills=models.TextField(blank=True)
    education=models.TextField(blank=True)
    experience=models.TextField(blank=True)

    def __str__(self):
        return self.user.email


class Company(models.Model):
    recruiter=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='company')
    name=models.CharField(max_length=150)
    description=models.TextField(blank=True)
    website=models.URLField(blank=True)
    location=models.CharField(max_length=100,blank=True)
    industry=models.CharField(max_length=100,blank=True)

    def __str__(self):
        return self.name