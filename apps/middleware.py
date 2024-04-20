from django.contrib.auth import logout
from django.urls import reverse
from django.http import HttpResponseRedirect

class AdminLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == reverse('login') or request.path == reverse('home') or request.path == reverse('passenger_details') or request.path == reverse('mybookings'):
            if request.user.is_authenticated and request.user.is_superuser:
                # If the user is a superuser and trying to access regular user pages,
                # force logout and redirect to admin login page
                logout(request)
                return HttpResponseRedirect(reverse('admin:login'))

        response = self.get_response(request)
        return response
    
