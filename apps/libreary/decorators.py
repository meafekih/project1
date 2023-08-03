
from .models import Author
from graphql import GraphQLError


def auth_required(func):
    def wrapper(root, info, **kwargs):
        user = info.context.user
        if not user.is_authenticated:
            raise GraphQLError('Autentication required')
        return func(root, info, **kwargs)
    return wrapper


def email_duplicate(func):
    def wrapper(cls, root, info, name, email, bio):
        same_email = Author.objects.filter(email=email)
        if same_email:
            raise GraphQLError('Email duplicate')
        return func(cls, root, info, name, email, bio)
    return wrapper

 
from functools import wraps

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
            raise GraphQLError('You are not Authorized!')
        return wrapper_func
    return decorator




#def wrapper_func(request, *args, **kwargs):