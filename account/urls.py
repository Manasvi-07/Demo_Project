from django.urls import path
from account.views import CreateUserView, AdminSignupView,UserRoleUpdateView, UserProfileUpdateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('auth/admin/signup', AdminSignupView.as_view(), name="Admin_signup"),
    path('auth/signup', CreateUserView.as_view(), name="Create_user"),
    path('auth/token', TokenObtainPairView.as_view(), name="User_login"),
    path('auth/token/refresh', TokenRefreshView.as_view(), name="Refresh_token"),
    path('user/profile', UserProfileUpdateView.as_view(), name="User_update_profile"),
    path('user/<int:pk>/role', UserRoleUpdateView.as_view(), name="User_role_update"),
]
