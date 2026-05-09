#!/usr/bin/env python3
"""
weather.py - CLI tool to fetch weather parameters using OpenWeather API.
"""

import os
import argparse
import requests
from dotenv import load_dotenv
from datetime import datetime

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather(city_id):
    """Fetch weather data from OpenWeatherMap using city ID."""
    url = f"http://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={API_KEY}&units=metric"
    response = requests.get(url).json()

    # Handle API errors
    if isinstance(response, dict) and "cod" in response and response["cod"] != 200:
        raise Exception(f"API error: {response.get('message')}")

    weather_info = {
        "city": response["name"],
        "temperature_min": response["main"]["temp_min"],
        "temperature_max": response["main"]["temp_max"],
        "temperature_current": response["main"]["temp"],
        "windspeed": response["wind"]["speed"],
        "humidity": response["main"]["humidity"],
        "clouds": response["clouds"]["all"],
        "pressure": response["main"]["pressure"],
        "sunrise": datetime.fromtimestamp(response["sys"]["sunrise"]).strftime("%H:%M:%S"),
        "sunset": datetime.fromtimestamp(response["sys"]["sunset"]).strftime("%H:%M:%S"),
    }
    return weather_info

def main():
    parser = argparse.ArgumentParser(description="Weather CLI Tool (OpenWeather)")
    parser.add_argument("city_id", help="City ID from OpenWeatherMap")
    args = parser.parse_args()

    print(f"\n🌤 Weather Report for City ID: {args.city_id}\n")
    weather = get_weather(args.city_id)
    for key, value in weather.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()
