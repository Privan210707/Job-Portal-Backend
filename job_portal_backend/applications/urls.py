from django.urls import path
from .views import (ApplicationCreateView,
                    CandidateApplicationListView,
                    RecruiterJobApplicationListView,
                    ApplicationStatusUpdateView,
                    ResumeAccessView)

urlpatterns = [
    path('',ApplicationCreateView.as_view()),
    path('my/',CandidateApplicationListView.as_view()),
    path('job/<int:job_id>/',RecruiterJobApplicationListView.as_view()),
    path('<int:pk>/status/',ApplicationStatusUpdateView.as_view()),
    path('<int:pk>/resume/',ResumeAccessView.as_view())
]
