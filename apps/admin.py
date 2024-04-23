from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import  Flight,Booking,Passenger,Payment,Help

@admin.register(Flight)
class FlightAdmin(ImportExportModelAdmin):
    list_display = ('airline', 'flight_number', 'departure_date', 'departure_time', 'arrival_time', 'from_location', 'to_location', 'price', 'class_type','total_seat','is_available')

admin.site.register(Passenger)
admin.site.register(Booking)
admin.site.register(Payment)
admin.site.register(Help)





    