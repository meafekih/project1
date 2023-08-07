from .exceptions import (EMAIL_DUPLICATE , AUTHENTICATION_REQUIRED,
EMAIL_REQUIRED, NAME_REQUIRED, FIELD_REQUIRED)
from functools import wraps


# this filter generic filter all fieds of model
def filter_resolver(model_type):
    def decorator(resolver_func):
        @wraps(resolver_func)
        def wrapper(self, info, **kwargs):
            queryset = resolver_func(self, info, **kwargs) 
            for n, v in kwargs.items():
                if n in model_type._meta.fields:
                    filter_args = {n: v}
                    queryset = queryset.filter(**filter_args)
            return queryset
        return wrapper
    return decorator

#from ..crm.schemas.customer import Customer
from functools import wraps

def auth_required(func):
    def wrapper(root, info, **kwargs):         
        user = info.context.user
        if not user.is_authenticated:
            raise AUTHENTICATION_REQUIRED        
        return func(root, info, **kwargs)
    return wrapper

def email_duplicate(model):
    def decorator(resolver_func):
        @wraps(resolver_func)
        def wrapper(self, info, **kwargs):
            model_filter = model.objects.filter(**{'email': kwargs.get('email')})
            """
            name = 'email'
            value = kwargs.get('email')
            filter_args = {name: value}             
            for name, value in kwargs.items():
                if name == 'email':
                    filter_args = {name: value}
                    break
            model_filter = model.objects.filter(**filter_args)
            """
            if model_filter:
                raise EMAIL_DUPLICATE                         
            return resolver_func(self, info, **kwargs)           
        return wrapper
    return decorator

def required_fields(*fields_kwargs):
    def decorator(resolver_func):
        @wraps(resolver_func)
        def wrapper(self, info, **kwargs):
            for field in fields_kwargs:
                value = kwargs.get(field)
                if value is None:
                    raise FIELD_REQUIRED(field.upper() + " "+"required") 
            return resolver_func(self, info, **kwargs)           
        return wrapper
    return decorator

