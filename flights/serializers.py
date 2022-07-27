from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

from .models import Booking, Flight


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ["destination", "time", "price", "id"]


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["flight", "date", "id"]


class BookingDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["flight", "date", "passengers", "id"]


class UpdateBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["date", "passengers"]


User = get_user_model()

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    #for token
    access =serializers.CharField(allow_blank=True, read_only=True)
    
    def validate(self, data):
        username = data.get ("username")
        password = data.get("password")
        try:
            user = User.objects.get(username=username) #does user exist in my database?
        except User.DoesNotExist:
            raise serializers. ValidationError ("Looks like user doesn't exist.. ")
        if not user.check_password(password):
            raise serializers.ValidationError ("Looks like password is incorrect..")
        
        #token code here
        
        payload = RefreshToken.for_user(user)
        token = str(payload.access_token)
        
        data["access"] = token
        
        return data

"""Create a Booking create API view:
It should use the same serializer as the update view.
The flight should get assigned automatically to the booking. The flight id should be retrieved from the url.
The user should get assigned automatically to the booking. The logged in user who is creating the booking should get assigned as the user.
Create a URL with name book-flight for this view and test it in postman.
"""
class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["flight", "date", "passengers"]

    def create(self, validated_data):
        flight = Flight.objects.get(id=self.context["view"].kwargs["flight_id"])
        return Booking.objects.create(flight=flight, **validated_data)