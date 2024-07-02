# myapp/views.py
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings


def get_ip():
    response = requests.get("https://api64.ipify.org?format=json").json()
    return response["ip"]


def get_location():
    ip_address = get_ip()
    response = requests.get(f"https://ipapi.co/{ip_address}/json/").json()
    location_data = {
        "ip": ip_address,
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name"),
    }
    return location_data


class Hello(APIView):
    def get(self, request):
        visitor_name = request.GET.get("visitor_name", "Guest")

        # Get location data using the get_location function
        location_data = get_location()
        location = location_data.get("city", "Unknown location")

        if location != "Unknown location":
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
            temperature = "unknown"

        greeting = f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {location}"

        response_data = {
            "client_ip": location_data["ip"],
            "location": location,
            "greeting": greeting,
        }

        return Response(response_data, status=status.HTTP_200_OK)
