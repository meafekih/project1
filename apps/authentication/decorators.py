from .exceptions import EMAIL_DUPLICATE
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





