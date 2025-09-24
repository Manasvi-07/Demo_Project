from django.db import models

class RoleChoices(models.TextChoices):
    ADMIN = 'admin', 'Admin'
    MANAGER = 'manager', 'Manager'
    DEVELOPER = 'developer', 'Developer'