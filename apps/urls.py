from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('login/', views.loginpage, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logoutUser, name='logout'),
    path('bookflight/', views.bookflight, name='bookflight'),
    path('passenger/', views.passenger_details, name='passenger_details'),
    path('payment/<int:booking_id>/<str:flight_fare>/', views.payment, name='payment'),
    path('payment_success/<int:booking_id>', views.payment_success, name='payment_success'),
    path('mybookings/', views.my_bookings, name='mybookings'),
    path('help/', views.help, name='help'),
    path('feedback/', views.feedback, name='feedback'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('error-404/', views.error_404, name='error_404'),
]
