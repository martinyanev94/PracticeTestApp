class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # This code will be executed for each request before reaching the view.
        # You can add your custom function here.
        # For example, let's say you want to log each request.
        print(f"User accessed URL: {request.path}")
        # manage_membership(request)

        # Continue processing the request.
        response = self.get_response(request)

        # This code will be executed for each response after the view has processed the request.
        # You can add custom response processing here if needed.

        return response
