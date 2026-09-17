from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.exceptions import PermissionDenied
from accounts.models import UserRole
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

class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Job.objects.all()
    
    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)

        # Candidates can view jobs but cannot edit/delete them
        if request.method == 'GET':
            return
        
        # Only recruiters can update/delete jobs
        if request.user.role != UserRole.RECRUITER:
            raise PermissionDenied(
                "Only recruiters can update or delete jobs."
            )

        # Only the recruiter who owns the job can update/delete it
        if obj.company.recruiter != request.user:
            raise PermissionDenied(
                "You can only modify your own jobs."
            )