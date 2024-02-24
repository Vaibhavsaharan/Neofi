from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.conf import settings

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.login_url = getattr(settings, 'LOGIN_URL', '/accounts/login/')

    def __call__(self, request):
        response = self.process_request(request)
        if response:
            return response
        return self.get_response(request)

    def process_request(self, request):
        print('processing', request.user)
        if not request.user.is_authenticated:
            # Redirect to login page
            return redirect(self.login_url)
        return None