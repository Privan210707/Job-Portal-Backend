from rest_framework import serializers
from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    candidate_name = serializers.CharField(
        source='candidate.user.username',
        read_only=True
    )
    job_title = serializers.CharField(
        source='job.title',
        read_only=True
    )
    company_name = serializers.CharField(
        source='job.company.name',
        read_only=True
    )

    class Meta:
        model = Application
        fields = [
            'id',
            'candidate',
            'candidate_name',
            'job',
            'job_title',
            'company_name',
            'cover_letter',
            'resume',
            'status',
            'applied_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'candidate',
            'candidate_name',
            'job_title',
            'company_name',
            'status',
            'applied_at',
            'updated_at',
        ]

    def validate_resume(self, file):
        if file is None:
            return file

        allowed_types = [
            'application/pdf',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        ]
        max_size = 5 * 1024 * 1024  # 5 MB
        if file.content_type not in allowed_types:
            raise serializers.ValidationError(
                'Only PDF, DOC, and DOCX files are allowed.'
            )
        if file.size > max_size:
            raise serializers.ValidationError(
                'Resume file size must not exceed 5 MB.'
            )
        return file