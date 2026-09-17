from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, UserRole
from jobs.models import Job
from jobs.serializers import JobSerializer

class AdminOnlyPermission(permissions.BasePermission):
    message = "Only admins can access this resource."
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == UserRole.ADMIN
        )


class AdminUserListView(generics.ListAPIView):
    queryset = User.objects.all().order_by('-date_joined')
    permission_classes = [AdminOnlyPermission]
    def list(self, request, *args, **kwargs):
        users = self.get_queryset()
        data = [
            {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'is_blocked': user.is_blocked,
                'date_joined': user.date_joined,
            }
            for user in users
        ]
        return Response(data)


class BlockUserView(APIView):
    permission_classes = [AdminOnlyPermission]
    def patch(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {'detail': 'User not found.'},
                status=404
            )
        if user.role == UserRole.ADMIN:
            return Response(
                {'detail': 'Admin users cannot be blocked.'},
                status=400
            )
        user.is_blocked = True
        user.save(update_fields=['is_blocked'])
        return Response({
            'detail': 'User blocked successfully.',
            'user_id': user.id,
            'is_blocked': user.is_blocked,
        })


class UnblockUserView(APIView):
    permission_classes = [AdminOnlyPermission]
    def patch(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {'detail': 'User not found.'},
                status=404
            )
        user.is_blocked = False
        user.save(update_fields=['is_blocked'])
        return Response({
            'detail': 'User unblocked successfully.',
            'user_id': user.id,
            'is_blocked': user.is_blocked,
        })


class AdminJobListView(generics.ListAPIView):
    queryset = Job.objects.all().order_by('-created_at')
    permission_classes = [AdminOnlyPermission]

    def list(self, request, *args, **kwargs):
        jobs = self.get_queryset()
        data = [
            {
                'id': job.id,
                'title': job.title,
                'company': job.company.name,
                'location': job.location,
                'job_type': job.job_type,
                'is_active': job.is_active,
                'deadline': job.deadline,
                'created_at': job.created_at,
            }
            for job in jobs
        ]
        return Response(data)


class AdminJobManagementView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    permission_classes = [AdminOnlyPermission]
    serializer_class = JobSerializer    