# myapp/views.py
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings


class Hello(APIView):
    def get(self, request):
        visitor_name = request.GET.get("visitor_name", "Guest")

        # Fetch location based on client's IP address
        ip_response = requests.get(
            "http://ip-api.com/json/",
            params={"query": request.META.get("REMOTE_ADDR", "127.0.0.1")},
        )
        ip_data = ip_response.json()

        if ip_response.status_code == 200 and ip_data["status"] == "success":
            location = ip_data.get("city", "Unknown location")
            # Fetch the weather for the obtained location
            weather_response = requests.get(
                "http://api.weatherapi.com/v1/current.json",
                params={"key": settings.WEATHER_API_KEY, "q": location},
            )
            weather_data = weather_response.json()
            if weather_response.status_code == 200:
                temperature = weather_data["current"]["temp_c"]
            else:
                temperature = "unknown"
        else:
            location = "Unknown location"
            temperature = "unknown"

        greeting = f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {location}"

        response_data = {
            "client_ip": request.META.get("REMOTE_ADDR", "127.0.0.1"),
            "location": location,
            "greeting": greeting,
        }

        return Response(response_data, status=status.HTTP_200_OK)
