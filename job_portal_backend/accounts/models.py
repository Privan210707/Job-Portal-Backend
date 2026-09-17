from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class UserRole(models.TextChoices):
    CANDIDATE='CANDIDATE','Candidate'
    RECRUITER='RECRUITER','Recruiter'
    ADMIN='ADMIN','Admin'
class User(AbstractUser):
    email=models.EmailField(unique=True)
    role=models.CharField(max_length=20,choices=UserRole.choices,default=UserRole.CANDIDATE)
    is_blocked=models.BooleanField(default=False)
    
    def __str__(self):
            return self.email
