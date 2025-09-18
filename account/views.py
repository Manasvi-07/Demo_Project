from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from account.models import CustomUser
from account.permissions import IsAdminOrManager
from account.enums import RoleChoices
from account.serializers import UserSerializer, AdminSerializer
from account.utils import get_token_for_user

class AdminSignupView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        self.user = serializer.save(role = RoleChoices.ADMIN)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        token = get_token_for_user(self.user)
        response.data.update(token)
        return response

class UserSignupView(ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

    def get_permissions(self):
        if self.request.method == "POST":
            return [AllowAny()]
        return [IsAdminOrManager()]
    
    def perform_create(self, serializer):
        self.user = serializer.save()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        token = get_token_for_user(self.user)
        response.data.update(token)
        return response

class UserProfileUpdateView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
class UserRoleUpdateView(UpdateAPIView):
    serializer_class = AdminSerializer
    permission_classes = [IsAdminOrManager]
    queryset = CustomUser.objects.all()

    def perform_update(self, serializer):
        updater = self.request.user
        target_user = self.get_object()
        new_role = self.request.data.get('role')

        if updater.role == RoleChoices.MANAGER:
            if target_user.role == RoleChoices.DEVELOPER:
                raise PermissionDenied("Manager can update only developer")
            if new_role and new_role != RoleChoices.DEVELOPER:
                raise PermissionDenied("Manager can assigned only developer")
            
        serializer.save()