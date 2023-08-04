# decorators.py

from functools import wraps
def paginatation(dpage=0, dpage_size=0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            page = kwargs.pop('page', dpage)
            page_size = kwargs.pop('page_size', dpage_size)
            if ((page>0) & (page_size>0)):
                start_index = (page - 1) * page_size
                end_index = start_index + page_size
                queryset = func(*args, **kwargs)[start_index:end_index]
            else:
                queryset = func(*args, **kwargs)
            return queryset
        return wrapper
    return decorator