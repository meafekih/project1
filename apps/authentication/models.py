from django.db import models
from django.contrib.auth.models import AbstractUser

class EmailConfiguration(models.Model):
    # New fields for outgoing mail server
    smtp_server = models.CharField(max_length=255, blank=True)
    smtp_port = models.PositiveIntegerField(blank=True, null=True)
    # New fields for incoming mail server
    incoming_server = models.CharField(max_length=255, blank=True)
    incoming_port = models.PositiveIntegerField(blank=True, null=True)
    incoming_type = models.CharField(max_length=10, blank=True,
        choices=[('POP', 'POP'),('IMAP', 'IMAP'),('Local', 'Local'),])
    incoming_ssl = models.BooleanField(default=False)
    incoming_tls = models.BooleanField(default=False)


class ExtendUser(AbstractUser):
    email = models.EmailField(blank=False,max_length=255,verbose_name="email")
    email_conf = models.ForeignKey(EmailConfiguration, on_delete=models.SET_NULL
            , related_name='ExtendUser', null=True)
    app_password = models.CharField(max_length=255)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'

