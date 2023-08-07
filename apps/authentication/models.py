from django.db import models
from django.contrib.auth.models import User, AbstractUser

class ExtendUser(AbstractUser):
    email = models.EmailField(blank=False,max_length=255,verbose_name="email")

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'

 