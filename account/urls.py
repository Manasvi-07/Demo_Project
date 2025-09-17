from django.urls import path
from account.views import UserSignupView, AdminSignupView, UserRoleUpdateView, UserProfileUpdateView

urlpatterns = [
    path('signup/admin/', AdminSignupView.as_view(), name="Admin_signup"),
    path('signup/user/', UserSignupView.as_view(), name="Create_user"),
    path('user/profile/', UserProfileUpdateView.as_view(), name="User_update_profile"),
    path('user/role/<int:pk>/', UserRoleUpdateView.as_view(), name="User_role_update"),
]
