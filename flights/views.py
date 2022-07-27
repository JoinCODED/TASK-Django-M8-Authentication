import datetime

from rest_framework import generics

from flights import serializers
from flights.models import Booking, Flight


class FlightsList(generics.ListAPIView):
    queryset = Flight.objects.all()
    serializer_class = serializers.FlightSerializer


class BookingsList(generics.ListAPIView):
    serializer_class = serializers.BookingSerializer

    def get_queryset(self):
        return Booking.objects.filter(date__gte=datetime.date.today())


class BookingDetails(generics.RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = serializers.BookingDetailsSerializer
    lookup_url_kwarg = "booking_id"


class UpdateBooking(generics.RetrieveUpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = serializers.UpdateBookingSerializer
    lookup_url_kwarg = "booking_id"


class CancelBooking(generics.DestroyAPIView):
    queryset = Booking.objects.all()
    lookup_url_kwarg = "booking_id"



"""Create a Booking create API view:
It should use the same serializer as the update view.
The flight should get assigned automatically to the booking. The flight id should be retrieved from the url.
The user should get assigned automatically to the booking. The logged in user who is creating the booking should get assigned as the user.
Create a URL with name book-flight for this view and test it in postman.
"""
# class BookFlight(generics.CreateAPIView):
#     queryset = Booking.objects.all()
#     serializer_class = serializers.BookingCreateSerializer
#     lookup_url_kwarg = "flight_id"

#     def perform_create(self, serializer):
#         flight = Flight.objects.get(id=self.kwargs['flight_id'])
#         serializer.save(flight=flight, user=self.request.user)
