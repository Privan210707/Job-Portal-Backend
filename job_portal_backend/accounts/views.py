from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.

class HealthCheckView(APIView):
    def get(self,request):
        return Response({
            "status":"success",
            "message":"Job Portal Backend is running"
        })
