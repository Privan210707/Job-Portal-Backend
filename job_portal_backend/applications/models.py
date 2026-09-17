from django.db import models
from secure_storage import SecureResumeStorage

# Create your models here.

class ApplicationStatus(models.TextChoices):
    APPLIED = 'APPLIED', 'Applied'
    SHORTLISTED = 'SHORTLISTED', 'Shortlisted'
    INTERVIEW = 'INTERVIEW', 'Interview'
    REJECTED = 'REJECTED', 'Rejected'
    SELECTED = 'SELECTED', 'Selected'

class Application(models.Model):
    candidate = models.ForeignKey(
        'profiles.CandidateProfile',
        on_delete=models.CASCADE,
        related_name='applications'
    )
    job = models.ForeignKey(
        'jobs.Job',
        on_delete=models.CASCADE,
        related_name='applications'
    )
    cover_letter = models.TextField(
        blank=True
    )
    resume = models.FileField(
        upload_to='resumes/',
        storage=SecureResumeStorage(),
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=20,
        choices=ApplicationStatus.choices,
        default=ApplicationStatus.APPLIED
    )
    applied_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    class Meta:
        ordering = ['-applied_at']
        constraints = [
            models.UniqueConstraint(
                fields=['candidate', 'job'],
                name='unique_candidate_job_application'
            )
        ]
        indexes = [
            models.Index(fields=['candidate']),
            models.Index(fields=['job']),
            models.Index(fields=['status']),
            models.Index(fields=['applied_at']),
        ]

    def __str__(self):
        return f'{self.candidate.user.email} - {self.job.title}'