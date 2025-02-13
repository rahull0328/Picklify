from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from base.emails import sendAccountActivationEmail

# Create your models here.

class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    isEmailVerified = models.BooleanField(default=False)
    emailToken = models.CharField(max_length=100, null=True, blank=True, unique=True)
    profileImg = models.ImageField(upload_to="profile")
    
@receiver(post_save, sender= User)
def sendMailToken(sender, instance, created, **kwargs):
    try:
        if created:
            emailToken = str(uuid.uuid4())
            Profile.objects.create(user = instance, emailToken = emailToken )
            email = instance.email
            sendAccountActivationEmail(email, emailToken)
    except Exception as e:
        print("Error in Send Mail Token: ", e)    