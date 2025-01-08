from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel

# Create your models here.

class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    isEmailVerified = models.BooleanField(default=False)
    emailToken = models.CharField(max_length=100, null=True, blank=True)
    profileImg = models.ImageField(upload_to="profile")