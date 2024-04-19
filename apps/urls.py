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
    # Add more URLs for other functionalities as needed
]
