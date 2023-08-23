from django.urls import path
from .views import sendingEmail, fetchingEmails

urlpatterns = [
    path('send_email/', sendingEmail, name='send-email'),
    path('fetch_emails/', fetchingEmails, name='fetch-emails'),
]