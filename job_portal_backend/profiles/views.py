from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CandidateProfile, Company
from .serializers import CandidateProfileSerializer, CompanySerializer

# Create your views here.

class CandidateProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        profile, created = CandidateProfile.objects.get_or_create(
            user=request.user
        )
        serializer = CandidateProfileSerializer(profile)
        return Response(serializer.data)
    def put(self, request):
        profile, created = CandidateProfile.objects.get_or_create(
            user=request.user
        )
        serializer = CandidateProfileSerializer(
            profile,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class CompanyProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        company, created = Company.objects.get_or_create(
            recruiter=request.user
        )
        serializer = CompanySerializer(company)
        return Response(serializer.data)
    def put(self, request):
        company, created = Company.objects.get_or_create(
            recruiter=request.user
        )
        serializer = CompanySerializer(
            company,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
