
from .models import Author
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
    def wrapper(cls, root, info, name, email, bio):
        same_email = Author.objects.filter(email=email)
        if same_email:
            raise EMAIL_DUPLICATE
        return func(cls, root, info, name, email, bio)
    return wrapper


def allowed_user(allowed_roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper_func(root, info):
            user = info.context.user
            groups_list = list(user.groups.all().values_list('name', flat=True))
            for i in groups_list:
                for j in allowed_roles:
                    if i==j:
                        return view_func(root, info) 
            raise UNAUTHORIZED
        return wrapper_func
    return decorator


def validation():
    def decorator(view_func):
        @wraps(view_func)
        def wrapper_func(root, info):
            user = info.context.user
            if user:
                raise TypeError('User not fond')
            return view_func(root, info)
        return wrapper_func
    return decorator