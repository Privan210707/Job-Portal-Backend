from django.urls import path
from .views import HealthCheckView,RegisterView,CurrentUserView,CandidateTestView,RecruiterTestView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('health/',HealthCheckView.as_view()),
    path('register/',RegisterView.as_view()),
    path('login/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('me/',CurrentUserView.as_view()),
    path('candidate-test/',CandidateTestView.as_view()),
    path('recruiter-test/',RecruiterTestView.as_view()),
]
