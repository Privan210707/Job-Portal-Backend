from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response

from accounts.models import UserRole
from profiles.models import CandidateProfile
from .models import Application
from .serializers import ApplicationSerializer

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

class ApplicationCreateView(generics.CreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role != UserRole.CANDIDATE:
            raise PermissionDenied(
                "Only candidates can apply for jobs."
            )
        candidate_profile, created = CandidateProfile.objects.get_or_create(
            user=self.request.user
        )
        job_id = self.request.data.get('job')
        if Application.objects.filter(
            candidate=candidate_profile,
            job_id=job_id
        ).exists():
            raise ValidationError(
                "You have already applied for this job."
            )
        serializer.save(
            candidate=candidate_profile,
            status='APPLIED'
        )


class CandidateApplicationListView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role != UserRole.CANDIDATE:
            raise PermissionDenied(
                "Only candidates can view their applications."
            )
        candidate_profile, created = CandidateProfile.objects.get_or_create(
            user=self.request.user
        )
        return Application.objects.filter(
            candidate=candidate_profile
        )


class RecruiterJobApplicationListView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role != UserRole.RECRUITER:
            raise PermissionDenied(
                "Only recruiters can view job applications."
            )
        job_id = self.kwargs['job_id']
        return Application.objects.filter(
            job_id=job_id,
            job__company__recruiter=self.request.user
        )    

class ApplicationStatusUpdateView(generics.UpdateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['patch']

    def get_queryset(self):
        if self.request.user.role != UserRole.RECRUITER:
            raise PermissionDenied(
                "Only recruiters can update application status."
            )

        return Application.objects.filter(
            job__company__recruiter=self.request.user
        )

    def perform_update(self, serializer):
        status_value = self.request.data.get('status')

        allowed_statuses = [
            'APPLIED',
            'SHORTLISTED',
            'INTERVIEW',
            'REJECTED',
            'SELECTED'
        ]

        if status_value not in allowed_statuses:
            raise ValidationError({
                'status': 'Invalid application status.'
            })

        application = serializer.save(status=status_value)

        # Send WebSocket notification to the candidate
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            f'candidate_{application.candidate.user.id}',
            {
                'type': 'notification',
                'message': (
                    f'Your application for "{application.job.title}" '
                    f'has been updated to {status_value}.'
                ),
                'application_id': application.id,
                'status': status_value,
            }
        )

class ResumeAccessView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk):
        try:
            application = Application.objects.select_related(
                'candidate__user',
                'job__company__recruiter'
            ).get(pk=pk)
        except Application.DoesNotExist:
            return Response(
                {"detail": "Application not found."},
                status=404
            )
        is_candidate = (
            request.user.role == UserRole.CANDIDATE
            and application.candidate.user_id == request.user.id
        )
        is_recruiter = (
            request.user.role == UserRole.RECRUITER
            and application.job.company.recruiter_id == request.user.id
        )
        if not (is_candidate or is_recruiter):
            raise PermissionDenied(
                "You are not authorized to access this resume."
            )
        if not application.resume:
            return Response(
                {"detail": "No resume uploaded."},
                status=404
            )
        return Response({
            "resume_url": application.resume.url
        })       