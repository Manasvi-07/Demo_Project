from django.shortcuts import render
from rest_framework import generics, permissions
from account.models import CustomUser
from account.permissions import IsAdminOrManagerAddDeveloper, IsAdminOrManager
from account.enums import RoleChoices
from account.serializers import UserSerializer, AdminSerializer
from account.utils import get_token_for_user
from rest_framework.permissions import IsAuthenticated

class AdminSignupView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        self.user = serializer.save(role = RoleChoices.ADMIN)

    def create(self, request, *args, **kwargs):
        respone = super().create(request, *args, **kwargs)
        token = get_token_for_user(self.user)
        respone.data.update(token)
        return respone

class UserSignupView(generics.CreateAPIView, generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all().order_by("id")
    permission_classes = [IsAuthenticated, IsAdminOrManagerAddDeveloper]
    
    def perform_create(self, serializer):
        self.user = serializer.save()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        token = get_token_for_user(self.user)
        response.data.update(token)
        return response

class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
class UserRoleUpdateView(generics.UpdateAPIView):
    serializer_class = AdminSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]
    queryset = CustomUser.objects.all()

    def perform_update(self, serializer):
        updater = self.request.user
        target_user = self.get_object()
        new_role = self.request.data.get('role')

        if updater.role == RoleChoices.MANAGER:
            if target_user.role == RoleChoices.DEVELOPER:
                raise PermissionError("Manager can update only developer")
            if new_role and new_role != RoleChoices.DEVELOPER:
                raise PermissionError("Manager can assigned only developer")
            
        serializer.save()