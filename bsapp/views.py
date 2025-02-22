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


# print(get_location())


class Hello(APIView):
    def get(self, request):
        visitor_name = request.GET.get("visitor_name", "Guest")

        # Step 1: Get the client's public IP address
        ip_response = requests.get("https://api.ipify.org?format=json")
        client_ip = ip_response.json()["ip"]

        # Step 2: Use the client's IP address in the API call to IPify
        url = "https://geo.ipify.org/api/v2/country,city"
        params = {"apiKey": settings.IPIFY_KEY, "ipAddress": client_ip}

        response = requests.get(url, params=params)

        ip_data = response.json()

        if response.status_code == 200:
            # location = ip_data.get(["location"]["city"], "Unknown location")
            location = ip_data.get("location", {}).get("city", "Unknown location")

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
