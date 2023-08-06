from .exceptions import EMAIL_DUPLICATE , AUTHENTICATION_REQUIRED
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
        """ 
        user = info.context.user
        if not user.is_authenticated:
            raise AUTHENTICATION_REQUIRED
        """
        return func(root, info, **kwargs)
    return wrapper




def email_duplicate(func):
    def wrapper(cls, root, info, name, email):
        """ 
        same_email = Customer.objects.filter(email=email)
        if same_email:
            raise EMAIL_DUPLICATE
        """
        return func(cls, root, info, name, email)
    return wrapper





