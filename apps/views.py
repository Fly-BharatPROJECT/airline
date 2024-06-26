from django.shortcuts import render, redirect 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login ,logout
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.urls import reverse 
from django.http import JsonResponse
from .models import Flight,Booking,Passenger,Payment,Help,Feedback
from django.shortcuts import HttpResponse
from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import datetime
import random




def home(request):
    bookings = Booking.objects.all()
    booking_details = []

    
    for booking in bookings:
        try:
           
            payment = Payment.objects.get(booking_id=booking.pk)
            
            passengers = Passenger.objects.filter(booking=booking)
            flight = Flight.objects.get(id=booking.flight_id)
          
            booking_details.append({
                'booking': booking,
                'reference_number': payment.reference,
                'passengers': passengers,
                'fare': payment.amount,
                'flight': flight,
            })
        except Payment.DoesNotExist:
            num_passengers_deleted = Passenger.objects.filter(booking=booking).count()
            flight = Flight.objects.get(id=booking.flight_id)
            flight.total_seat += num_passengers_deleted
            flight.save()
            booking.delete()
    return render(request, 'home.html')

@csrf_protect
def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if user exists
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'User not found')
            return redirect('login')  
        
        # Check if user is active and authenticate
        if user is not None and user.is_active:
            authenticated_user = authenticate(request, username=username, password=password)
            if authenticated_user is not None:
                login(request, authenticated_user)
                return redirect('home')  
            else:
                messages.error(request, 'Incorrect password')
                return redirect('login')  
        else:
            messages.error(request, 'User is not active')
            return redirect('login') 

    return render(request, 'login.html') 

from .forms import CustomUserCreationForm

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


from .forms import CustomUserChangeForm

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form, 'user': request.user})


def logoutUser(request):
    logout(request)
    return redirect('home')

@login_required
def search_flight(request):
    if request.method == 'GET':
        from_location = request.GET.get('from')
        to_location = request.GET.get('to')
        departure_date = request.GET.get('departure_date')
        flight_class = request.GET.get('class')
        url = reverse('bookflight') + f'?from={from_location}&to={to_location}&departure_date={departure_date}&class={flight_class}'
        return redirect(url)

@login_required
def bookflight(request):
    if request.method == 'GET':
        # Retrieve the selected flight details from the request
        from_location = request.GET.get('from')
        to_location = request.GET.get('to')
        departure_date = request.GET.get('departure_date')
        flight_class = request.GET.get('class')
        today = datetime.now().date()
        available_flights = Flight.objects.filter(
            from_location=from_location,
            to_location=to_location,
            departure_date=departure_date,
            class_type=flight_class 
        )
        
        context = {
            'from_location': from_location,
            'to_location': to_location,
            'departure_date': departure_date,
            'class_type': flight_class,  
            'available_flights': available_flights,
            'today': today,
        }
        
        return render(request, 'bookflight.html', context)






    

def generate_reference_number():
    """Generate a unique 16-digit reference number."""
    return ''.join(str(random.randint(0, 9)) for _ in range(16))

@login_required
def payment(request, booking_id, flight_fare):
    if request.method == 'POST':
        payment_date = timezone.now() 
        reference_number = generate_reference_number()
        amount = flight_fare  
        paid = 'pass'  

        payment = Payment.objects.create(
            booking_id=booking_id,
            reference=reference_number,
            amount=amount,
            payment_date=payment_date,
            paid=paid
        )        
        return redirect('payment_success',booking_id=booking_id)  
    else:
        context = {
            'booking_id': booking_id,
            'flight_fare': flight_fare,
        }
        return render(request, 'payment.html', context)
    

    

@login_required
def payment_success(request, booking_id):
    # Retrieve the booking object from the database
    booking = get_object_or_404(Booking, pk=booking_id)

    payment = get_object_or_404(Payment, booking_id=booking_id)
    passengers = Passenger.objects.filter(booking=booking)
    flight = get_object_or_404(Flight, id=booking.flight_id)
    # Pass the booking details, reference number, and passenger details to the template
    context = {
        'booking': booking,
        'reference_number': payment.reference,
        'passengers': passengers,
        'fare':payment,
        'flight':flight,
        
    }
    return render(request, 'payment_success.html', context)


@login_required
def my_bookings(request):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')  
        
        booking = Booking.objects.get(pk=booking_id)
        payment = Payment.objects.get(booking_id=booking_id)
        passengers_deleted = Passenger.objects.filter(booking=booking).count()
        flight = Flight.objects.get(id=booking.flight_id)
            
        flight.total_seat += passengers_deleted
        flight.save()
            
        booking.delete()
        payment.delete()
            
        return render(request,'home.html')
    else:
        user = request.user
        bookings = Booking.objects.filter(user=user)
        booking_details = []

        for booking in bookings:
            try:
                payment = Payment.objects.get(booking_id=booking.pk)
                passengers = Passenger.objects.filter(booking=booking)
                flight = Flight.objects.get(id=booking.flight_id)
                booking_details.append({
                    'booking': booking,
                    'reference_number': int(payment.reference),
                    'passengers': passengers,
                    'fare': payment,
                    'flight': flight,
                })
            except Payment.DoesNotExist:
                passengers_deleted = Passenger.objects.filter(booking=booking).count()
                flight = Flight.objects.get(id=booking.flight_id)
                flight.total_seat += passengers_deleted
                flight.save()
                booking.delete()
            
        context = {
            'booking_details': booking_details,
        }
        return render(request, 'mybookings.html', context)



@login_required
def passenger_details(request):
    if request.method == 'POST':
        contact_number = request.POST.get('contact_number')
        email = request.POST.get('email')
        fare_str = request.POST.get("total_fare")
        fare = Decimal(fare_str)
        departure_date = request.POST.get('departure_date')
        class_type = request.POST.get('class_type')        
        flight_id = request.POST.get('flight_id')    
        flight = get_object_or_404(Flight, id=flight_id)   
        booking = Booking.objects.create(  
            user=request.user,          
            departure_date=departure_date,
            class_type=class_type,
            flight_fare=fare,
            flight=flight
        ) 

        available_seats = generate_seat_numbers(flight_id,4)
        
        passenger_index = 1
        while True:
            passenger_name = request.POST.get(f'passenger_name{passenger_index}')
            if not passenger_name:  # If no name is provided, stop the loop
                break
            passenger_age = request.POST.get(f'passenger_age{passenger_index}')
            passenger_gender = request.POST.get(f'passenger_gender{passenger_index}')
            # Assign the first available seat to the passenger
            if available_seats:
                seat = available_seats.pop(0)
            else:
                # If no available seats, handle accordingly (redirect to another page or show a message)
                return HttpResponse("No available seats for this flight.")

            Passenger.objects.create(
                booking=booking,
                name=passenger_name,
                age=passenger_age,
                gender=passenger_gender,
                contact_number=contact_number,
                email=email,
                flight_id=flight_id, 
                seat=seat
            )
            passenger_index += 1
        booked_seats = Passenger.objects.filter(booking=booking).count()

        flightt = Flight.objects.get(id=flight_id)
        flightt.total_seat -= booked_seats
        flightt.save()
        
        # Redirect to the payment page
        return redirect('payment', booking_id=booking.pk, flight_fare=fare)
    else:
        # Retrieve flight details from the query parameters
        from_location = request.GET.get('from_location')
        to_location = request.GET.get('to_location')
        departure_date = request.GET.get('departure_date')
        class_type = request.GET.get('class_type')
        flight_fare = request.GET.get('flight_fare')
        flight_id = request.GET.get('flight_id')
        # Pass flight details to the template context
        context = {
            'from_location': from_location,
            'to_location': to_location,
            'departure_date': departure_date,
            'class_type': class_type,
            'flight_fare': flight_fare,
            'flight_id': flight_id,
        }
        # Render the form template
        return render(request, 'passenger_details.html', context)

def generate_seat_numbers(flight_id, total_seats):
    alphabet = 'ABC'
    available_seats = []
    count = 0
    for letter in alphabet:
        for i in range(1, 4):
            seat = f"{letter}{i}"
            if not Passenger.objects.filter(flight_id=flight_id, seat=seat).exists():
                available_seats.append(seat)
                count += 1
                if count == total_seats:
                    return available_seats
            if count == total_seats:
                return available_seats
    return available_seats

@login_required
def help(request):
    if request.method == 'POST':
       email=request.POST.get('email')
       issue=request.POST.get('issue')
       subject=request.POST.get('subject')
       help=Help.objects.create(
           user=request.user,
           email=email,
           issue=issue,
           subject=subject,
       )
       messages.success(request, "Issue Submited Successfully ")
       return render(request,'help.html')
    else:
        return render(request,'help.html')  


def feedback(request):
    if request.method == 'POST':
       email=request.POST.get('email')
       subject=request.POST.get('subject')
       help=Feedback.objects.create(
           email=email,
           subject=subject,
       )
       messages.success(request, "Issue Submited Successfully ")
       return render(request,'feedback.html')
    else:
        return render(request,'feedback.html')  


def aboutus(request):
    return render(request,'AboutUs.html')


def error_404(request, exception):
    return render(request, '404.html', status=404)
