from rest_framework import serializers
from .models import CustomUser
from .enums import RoleChoices

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email','password','role']

    def validate_role(self, value):
        user = self.context['request'].user

        if user.is_authenticated and user.role == RoleChoices.MANAGER and value != RoleChoices.DEVELOPER:
            raise serializers.ValidationError("Manager can create only Developers")
        return value
    
    def create(self, validated_data):
        request = self.context['request']
        if request and request.user.is_authenticated:
            if request.user.role == RoleChoices.MANAGER:
                validated_data['role'] = RoleChoices.DEVELOPER
        return CustomUser.objects.create_user(**validated_data)
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)
        instance.save()
        return instance
    
class AdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'email','password','role']
        