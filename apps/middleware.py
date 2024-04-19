# middleware.py

from django.contrib.auth import logout,login
from django.urls import reverse
from django.http import HttpResponseRedirect

class AdminLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if user is authenticated
        if request.user.is_authenticated and request.user.is_superuser:
            # Check if the user is a superuser and trying to access the regular login page or the homepage
            if request.user.is_superuser and (request.path == reverse('login') or request.path == reverse('home') or  request.path == reverse('passenger_details') or request.path == reverse('mybookings') ):
                logout(request)  # Log out the superuser attempting to access the regular login page or homepage
                return HttpResponseRedirect(reverse('admin:login'))  # Redirect superuser to admin login page
                     
        response = self.get_response(request)
        return response
