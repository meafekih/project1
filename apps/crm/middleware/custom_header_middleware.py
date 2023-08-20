 
#The request comes in from the client and is passed through each middleware
#class in the order they are listed in the MIDDLEWARE setting.


class CustomHeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        print('Start Middleware')
    
    def __call__(self, request):
        response = self.get_response(request)
        print('Call Middleware') 
        # Check if the request has a custom header
        custom_header_value = request.META.get('HTTP_X_CUSTOM_HEADER')
        if custom_header_value:
            # Add a custom response header
            response['X-Custom-Response-Header'] = f'Hello from custom middleware! Request header value: {custom_header_value}'
        
        return response

# myapp/graphql_middleware.py

import time

class GraphQLLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        end_time = time.time()

        if 'application/json' in request.META.get('HTTP_ACCEPT', ''):
            content_type = 'json'
        else:
            content_type = 'other'
        
        if 'graphql' in request.POST:
            query = request.POST['graphql']
        else:
            query = 'Not a GraphQL query'
        
        processing_time = end_time - start_time
        print(f"GraphQL {content_type} query took {processing_time:.6f} seconds: {query}")

        return response

