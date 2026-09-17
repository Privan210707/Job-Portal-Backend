from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import RegisterSerializer
from .permissions import IsCandidate,IsRecruiter
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.

class HealthCheckView(APIView):
    def get(self,request):
        return Response({
            "status":"success",
            "message":"Job Portal Backend is running"
        })

class RegisterView(APIView):
    authentication_classes=[]
    permission_classes=[]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "message": "User registered successfully",
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "role": user.role,
                    }
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
class CurrentUserView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        user=request.user
        return Response({
            "id":user.id,
            "username":user.username,
            "email":user.email,
            "role":user.role,
        })

class CandidateTestView(APIView):
    permission_classes = [IsCandidate]
    def get(self, request):
        return Response({
            "message": "Candidate access granted",
            "role": request.user.role,
        })

class RecruiterTestView(APIView):
    permission_classes = [IsRecruiter]
    def get(self, request):
        return Response({
            "message": "Recruiter access granted",
            "role": request.user.role,
        })


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response(
                {'detail': 'Refresh token is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {'detail': 'Logout successful.'},
                status=status.HTTP_205_RESET_CONTENT
            )
        except Exception:
            return Response(
                {'detail': 'Invalid or already blacklisted refresh token.'},
                status=status.HTTP_400_BAD_REQUEST
            )    