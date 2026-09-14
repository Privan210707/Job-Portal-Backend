from rest_framework import serializers
from .models import CandidateProfile, Company

class CandidateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateProfile
        fields = [
            'id',
            'phone',
            'bio',
            'location',
            'skills',
            'education',
            'experience',
        ]

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            'id',
            'name',
            'description',
            'website',
            'location',
            'industry',
        ]