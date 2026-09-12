from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    CANDIDATE='CANDIDATE','Candidate'
    RECRUITER='RECRUITER','Recruiter'
    ADMIN='ADMIN','Admin'
class Role(models.TextChoices):
    email=models.EmailField(unique=True)
    role=models.CharField(max_length=20,choices=Role.choices,default=Role.CANDIDATE)

    def __str__(self):
            return self.email
