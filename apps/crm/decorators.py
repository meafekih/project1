from .models import Customer
from .exceptions import EMAIL_DUPLICATE, AUTHENTICATION_REQUIRED, UNAUTHORIZED
from functools import wraps

def auth_required(func):
    def wrapper(root, info, **kwargs):
        user = info.context.user
        if not user.is_authenticated:
            raise AUTHENTICATION_REQUIRED
        return func(root, info, **kwargs)
    return wrapper


def email_duplicate(func):
    def wrapper(cls, root, info, name, email):
        same_email = Customer.objects.filter(email=email)
        if same_email:
            raise EMAIL_DUPLICATE
        return func(cls, root, info, name, email)
    return wrapper


