

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import User, UserRole
from profiles.models import CandidateProfile, Company
from jobs.models import Job
from django.utils import timezone
from datetime import timedelta


class JobPortalAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()

        # Candidate
        self.candidate = User.objects.create_user(
            username="candidate1",
            email="candidate@test.com",
            password="Candidate@123",
            role=UserRole.CANDIDATE
        )

        # Recruiter
        self.recruiter = User.objects.create_user(
            username="recruiter1",
            email="recruiter@test.com",
            password="Recruiter@123",
            role=UserRole.RECRUITER
        )

        # Admin
        self.admin = User.objects.create_superuser(
            username="admin1",
            email="admin@test.com",
            password="Admin@123",
        )
        self.admin.role = UserRole.ADMIN
        self.admin.save()

        # Candidate profile
        self.candidate_profile = CandidateProfile.objects.create(
            user=self.candidate,
            phone="9876543210",
            skills="Python, Django",
            education="B.Tech CSE",
            location="Noida"
        )

        # Company
        self.company = Company.objects.create(
            recruiter=self.recruiter,
            name="Test Company",
            description="Test company",
            website="https://example.com",
            location="Noida",
            industry="Technology"
        )

        # Job
        self.job = Job.objects.create(
            company=self.company,
            title="Python Developer",
            description="Python Django Developer",
            skills="Python, Django, REST API",
            location="Noida",
            job_type="FULL_TIME",
            experience_min=0,
            experience_max=2,
            salary_min=30000,
            salary_max=60000,
            deadline=timezone.now() + timedelta(days=30),
            is_active=True
        )

    # -------------------------------------------------
    # 1. REGISTRATION
    # -------------------------------------------------

    def test_candidate_registration(self):
        response = self.client.post(
            "/api/accounts/register/",
            {
                "username": "newcandidate",
                "email": "newcandidate@test.com",
                "password": "NewCandidate@123",
                "role": "CANDIDATE"
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # -------------------------------------------------
    # 2. LOGIN
    # -------------------------------------------------

    def test_login(self):
        response = self.client.post(
            "/api/accounts/login/",
            {
                "username": "candidate1",
                "password": "Candidate@123"
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    # -------------------------------------------------
    # 3. CURRENT USER
    # -------------------------------------------------

    def test_current_user(self):
        self.client.force_authenticate(user=self.candidate)

        response = self.client.get("/api/accounts/me/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "candidate@test.com")

    # -------------------------------------------------
    # 4. CANDIDATE PROFILE
    # -------------------------------------------------

    def test_candidate_profile(self):
        self.client.force_authenticate(user=self.candidate)

        response = self.client.get("/api/profiles/candidate/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # -------------------------------------------------
    # 5. COMPANY PROFILE
    # -------------------------------------------------

    def test_company_profile(self):
        self.client.force_authenticate(user=self.recruiter)

        response = self.client.get("/api/profiles/company/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # -------------------------------------------------
    # 6. JOB LIST
    # -------------------------------------------------

    def test_job_list(self):
        self.client.force_authenticate(user=self.candidate)

        response = self.client.get("/api/jobs/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # -------------------------------------------------
    # 7. JOB SEARCH
    # -------------------------------------------------

    def test_job_search(self):
        self.client.force_authenticate(user=self.candidate)

        response = self.client.get(
            "/api/jobs/?search=Python"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # -------------------------------------------------
    # 8. RECRUITER CREATES JOB
    # -------------------------------------------------

    def test_recruiter_create_job(self):
        self.client.force_authenticate(user=self.recruiter)

        response = self.client.post(
            "/api/jobs/",
            {
                "title": "Backend Developer",
                "description": "Django backend developer",
                "skills": "Python, Django",
                "location": "Delhi",
                "job_type": "FULL_TIME",
                "experience_min": 0,
                "experience_max": 2,
                "salary_min": 30000,
                "salary_max": 50000,
                "deadline": (
                    timezone.now() + timedelta(days=30)
                ).isoformat(),
                "is_active": True
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # -------------------------------------------------
    # 9. CANDIDATE APPLIES
    # -------------------------------------------------

    def test_candidate_apply(self):
        self.client.force_authenticate(user=self.candidate)

        response = self.client.post(
            "/api/applications/",
            {
                "job": self.job.id,
                "cover_letter": "I am interested in this job."
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # -------------------------------------------------
    # 10. DUPLICATE APPLICATION
    # -------------------------------------------------

    def test_duplicate_application(self):
        self.client.force_authenticate(user=self.candidate)

        # First application
        self.client.post(
            "/api/applications/",
            {
                "job": self.job.id,
                "cover_letter": "First application"
            },
            format="json"
        )

        # Second application
        response = self.client.post(
            "/api/applications/",
            {
                "job": self.job.id,
                "cover_letter": "Duplicate application"
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # -------------------------------------------------
    # 11. CANDIDATE VIEWS OWN APPLICATIONS
    # -------------------------------------------------

    def test_candidate_application_list(self):
        self.client.force_authenticate(user=self.candidate)

        response = self.client.get(
            "/api/applications/my/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # -------------------------------------------------
    # 12. RECRUITER VIEWS APPLICATIONS
    # -------------------------------------------------

    def test_recruiter_application_list(self):
        self.client.force_authenticate(user=self.candidate)

        # Create application
        self.client.post(
            "/api/applications/",
            {
                "job": self.job.id,
                "cover_letter": "Please consider my application."
            },
            format="json"
        )

        self.client.force_authenticate(user=self.recruiter)

        response = self.client.get(
            f"/api/applications/job/{self.job.id}/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # -------------------------------------------------
    # 13. RECRUITER UPDATES APPLICATION STATUS
    # -------------------------------------------------

    def test_recruiter_update_application_status(self):
        self.client.force_authenticate(user=self.candidate)

        response = self.client.post(
            "/api/applications/",
            {
                "job": self.job.id,
                "cover_letter": "My application."
            },
            format="json"
        )

        application_id = response.data["id"]

        self.client.force_authenticate(user=self.recruiter)

        response = self.client.patch(
            f"/api/applications/{application_id}/status/",
            {
                "status": "SHORTLISTED"
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "SHORTLISTED")

    # -------------------------------------------------
    # 14. CANDIDATE CANNOT CREATE JOB
    # -------------------------------------------------

    def test_candidate_cannot_create_job(self):
        self.client.force_authenticate(user=self.candidate)

        response = self.client.post(
            "/api/jobs/",
            {
                "title": "Unauthorized Job",
                "description": "Test",
                "skills": "Python",
                "location": "Noida",
                "job_type": "FULL_TIME",
                "experience_min": 0,
                "experience_max": 1,
                "salary_min": 20000,
                "salary_max": 30000,
                "deadline": (
                    timezone.now() + timedelta(days=30)
                ).isoformat()
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    # -------------------------------------------------
    # 15. UNAUTHENTICATED USER CANNOT ACCESS JOBS
    # -------------------------------------------------

    def test_unauthenticated_access(self):
        self.client.force_authenticate(user=None)

        response = self.client.get("/api/jobs/")

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    # -------------------------------------------------
    # 16. ADMIN CAN VIEW USERS
    # -------------------------------------------------

    def test_admin_users(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.get(
            "/api/accounts/admin/users/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    # -------------------------------------------------
    # 17. ADMIN CAN VIEW JOBS
    # -------------------------------------------------

    def test_admin_jobs(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.get(
            "/api/accounts/admin/jobs/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )