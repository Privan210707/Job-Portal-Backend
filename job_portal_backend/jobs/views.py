from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.exceptions import PermissionDenied

from .models import Job
from .serializers import JobSerializer

# Create your views here.

class JobListCreateView(generics.ListCreateAPIView):
    queryset = Job.objects.filter(is_active=True)
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]
    # Exact filters
    filterset_fields = [
        'location',
        'job_type',
        'experience_min',
        'experience_max',
    ]
    # Keyword search
    search_fields = [
        'title',
        'description',
        'skills',
        'location',
    ]
    # Sorting
    ordering_fields = [
        'created_at',
        'salary_min',
        'salary_max',
        'experience_min',
    ]
    ordering = ['-created_at']
    def perform_create(self, serializer):
        if self.request.user.role != 'RECRUITER':
            raise PermissionDenied("Only recruiters can create jobs.")

        company = self.request.user.company
        serializer.save(company=company)