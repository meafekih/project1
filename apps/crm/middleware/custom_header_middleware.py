# myapp/custom_header_middleware.py

class CustomHeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Check if the request has a custom header
        custom_header_value = request.META.get('HTTP_X_CUSTOM_HEADER')
        if custom_header_value:
            # Add a custom response header
            response['X-Custom-Response-Header'] = f'Hello from custom middleware! Request header value: {custom_header_value}'
        
        return response

