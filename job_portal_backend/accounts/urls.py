from django.urls import path
from .views import HealthCheckView,RegisterView,CurrentUserView,CandidateTestView,RecruiterTestView,LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from .admin_views import (AdminUserListView,BlockUserView,UnblockUserView,AdminJobListView,AdminJobManagementView)

urlpatterns = [
    path('health/',HealthCheckView.as_view()),
    path('register/',RegisterView.as_view()),
    path('login/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('me/',CurrentUserView.as_view()),
    path('candidate-test/',CandidateTestView.as_view()),
    path('recruiter-test/',RecruiterTestView.as_view()),
    path('admin/users/',AdminUserListView.as_view()),
    path('admin/users/<int:pk>/block/',BlockUserView.as_view()),
    path('admin/users/<int:pk>/unblock/',UnblockUserView.as_view()),
    path('admin/jobs/',AdminJobListView.as_view()),
    path('admin/jobs/<int:pk>/',AdminJobManagementView.as_view()),
    path('logout/',LogoutView.as_view()),
    path('login/refresh/',TokenRefreshView.as_view())
]
