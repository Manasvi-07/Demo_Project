from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [ 
    path('token/', TokenObtainPairView.as_view(), name="User_login"),
    path('token/refresh/', TokenRefreshView.as_view(), name="Refresh_token"),
]