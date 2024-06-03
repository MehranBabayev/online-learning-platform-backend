from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegistrationAPIView, LoginAPIView, LogoutAPIView, ProfileDetailAPIView, StudentProfileDetailAPIView, InstructorProfileDetailAPIView, PasswordResetAPIView, PasswordResetConfirmAPIView, ActivateAccountView

urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password-reset/', PasswordResetAPIView.as_view(), name='password-reset'),
    path('password-reset-confirm/', PasswordResetConfirmAPIView.as_view(), name='password-reset-confirm'),
    path('profile/', ProfileDetailAPIView.as_view(), name='profile-detail'),
    path('profile/student/', StudentProfileDetailAPIView.as_view(), name='student-profile-detail'),
    path('profile/instructor/', InstructorProfileDetailAPIView.as_view(), name='instructor-profile-detail'),
    path('activate/', ActivateAccountView.as_view(), name='activate'),  
]
