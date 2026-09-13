from django.db import models

# Create your models here.

class JobType(models.TextChoices):
    FULL_TIME = 'FULL_TIME', 'Full Time'
    PART_TIME = 'PART_TIME', 'Part Time'
    CONTRACT = 'CONTRACT', 'Contract'
    INTERNSHIP = 'INTERNSHIP', 'Internship'

class Job(models.Model):
    company = models.ForeignKey(
        'profiles.Company',
        on_delete=models.CASCADE,
        related_name='jobs'
    )
    title = models.CharField(max_length=150)
    description = models.TextField()
    skills = models.TextField()
    location = models.CharField(max_length=100)
    job_type = models.CharField(
        max_length=20,
        choices=JobType.choices
    )
    experience_min = models.PositiveIntegerField(default=0)
    experience_max = models.PositiveIntegerField(
        null=True,
        blank=True
    )
    salary_min = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )
    salary_max = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['location']),
            models.Index(fields=['job_type']),
            models.Index(fields=['experience_min']),
            models.Index(fields=['salary_min']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return self.title