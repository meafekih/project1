from django.urls import path
from .views import sendingEmail

urlpatterns = [
    path('emailing/', sendingEmail, name='emailing'),
]