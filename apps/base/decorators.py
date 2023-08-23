from .exceptions import (EMAIL_DUPLICATE , AUTHENTICATION_REQUIRED,
 FIELD_REQUIRED, MANY_VALUES_RETURNED, VALUE_NOT_EXIST)
from functools import wraps
from django.http import JsonResponse


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


def Rest_auth_required(func):
    def wrapper(request):         
        user = request.user
        if not user.is_authenticated:
            return JsonResponse(
            {"message": AUTHENTICATION_REQUIRED.default_message},
            status=500
            )         
        return func(request)
    return wrapper

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


def unique_instance(model):
    def decorator(resolver_func):
        @wraps(resolver_func)
        def wrapper(self, info, **kwargs):
            count = len(model.objects.filter(**kwargs))
            if count >1:
                raise MANY_VALUES_RETURNED       
            if count ==0:
                 raise VALUE_NOT_EXIST
            return resolver_func(self, info, **kwargs)           
        return wrapper
    return decorator

def download(path, filename):
    def decorator(resolver_func):
        @wraps(resolver_func)
        def wrapper(self, info, **kwargs): 

            file_path = f'{path}/{filename}'

            
            try:
                with open(file_path, 'rb') as file:
                    file_data = file.read()
                    return file_data.encode('base64').decode()  
            except FileNotFoundError:
                return None   


            return resolver_func(self, info, **kwargs)           
        return wrapper
    return decorator