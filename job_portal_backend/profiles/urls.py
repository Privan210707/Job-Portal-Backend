from django.urls import path
from .views import CandidateProfileView,CompanyProfileView

urlpatterns = [
    path('candidate/',CandidateProfileView.as_view()),
    path('company/',CompanyProfileView.as_view()),
]
