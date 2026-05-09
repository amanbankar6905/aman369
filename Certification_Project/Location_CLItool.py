#!/usr/bin/env python3
"""
location.py - Command line utility to fetch location parameters
using OpenWeatherMap Geocoding API.
"""

import argparse
import os
import requests
from dotenv import load_dotenv
load_dotenv()
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
print(OPENWEATHER_API_KEY)  # should print your key, not None

# Load API key from .env file
load_dotenv()
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")


def location_search(place, limit=1):
    #url = f"https://api.openweathermap.org/geo/1.0/direct?q={place}&limit={limit}&appid={OPENWEATHER_API_KEY}"
    url = f"https://api.openweathermap.org/geo/1.0/direct?q={place}&limit={limit}&appid={OPENWEATHER_API_KEY}"
    #url = f"http://api.openweathermap.org/geo/1.0/direct?q={place}&limit={limit}&appid={OPENWEATHER_API_KEY}"
    response = requests.get(url).json()

    # Debug
    print("DEBUG: Response =", response)

    # Handle API error
    if isinstance(response, dict) and "cod" in response:
        raise Exception(f"API error: {response.get('message')}")

    if not response:
        raise Exception(f"No location data found for '{place}'")

    locations = []
    for loc in response:
        location_data = {
            "name": loc.get("name"),
            "latitude": loc.get("lat"),
            "longitude": loc.get("lon"),
            "country": loc.get("country"),
            "state": loc.get("state")
        }
        locations.append(location_data)

    return locations


def main():
    parser = argparse.ArgumentParser(description="Location CLI Tool (OpenWeather Geocoding)")
    parser.add_argument("place", help="Place name")
    parser.add_argument("-l", "--limit", type=int, default=1,
                        help="Number of location results to fetch (default: 1)")
    args = parser.parse_args()

    print(f"\n Location parameters for: {args.place}\n")
    locations = location_search(args.place, args.limit)
    for i, loc in enumerate(locations, start=1):
        print(f"{i}. Name: {loc['name']}, Country: {loc['country']}, State: {loc.get('state')}")
        print(f"   Latitude: {loc['latitude']}, Longitude: {loc['longitude']}\n")


if __name__ == "__main__":
    main()
