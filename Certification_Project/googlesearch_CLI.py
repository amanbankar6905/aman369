#!/usr/bin/env python3
import os
import argparse
import webbrowser

from dotenv import load_dotenv
from serpapi import GoogleSearch
from datetime import datetime
import requests
import webbrowser



# Load environment variables
load_dotenv()

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")


def get_coordinates(city):
    """Return latitude and longitude for a given city using OpenWeatherMap Geocoding API."""
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={OPENWEATHER_API_KEY}"
    response = requests.get(url).json()

    if not response:
        raise Exception(f"City '{city}' not found.")

    lat = response[0]["lat"]
    lon = response[0]["lon"]
    return lat, lon

def google_search(query, num, open_browser=False, choose_result=None):
    params = {"q": query, "num": num, "api_key": SERPAPI_API_KEY}
    search = GoogleSearch(params)
    results = search.get_dict()

    links = []
    print(f"\nTop {num} results for: {query}\n")
    for i, res in enumerate(results.get("organic_results", []), start=1):
        title = res.get("title")
        link = res.get("link")
        links.append(link)
        print(f"{i}. {title} - {link}")

    # Browser opening logic
    if open_browser and links:
        if choose_result and 1 <= choose_result <= len(links):
            print(f"\nOpening result {choose_result} in your browser...")
            webbrowser.open_new_tab(links[choose_result - 1])
        else:
            print("\nOpening first result in your browser...")
            webbrowser.open_new_tab(links[0])

def get_weather(city):
    """Fetch weather forecast using latitude and longitude."""
    lat, lon = get_coordinates(city)
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url).json()

    if response.get("cod") != 200:
        raise Exception(f"Error fetching weather: {response.get('message')}")

    weather_info = {
        "city": response["name"],
        "latitude": lat,
        "longitude": lon,
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

def location_search(city):
    # Example using SerpAPI for location info
    # url =f"http://api.openweathermap.org/geo/1.0/direct?q=London&limit=5&appid={API key}"
    params = {"q": city, "api_key": OPENWEATHER_API_KEY}
    search = GoogleSearch(params)
    results = search.get_dict()
    """Return city location details (lat/lon) for reuse."""
    lat, lon = get_coordinates(city)
    return {"city": city, "latitude": lat, "longitude": lon}

    """if "knowledge_graph" in results:
        info = results["knowledge_graph"]
        print(f"Location: {info.get('title')}")
        print(f"Description: {info.get('description')}")
    else:
        print("No location info found.")"""

def main():
    parser = argparse.ArgumentParser(description="Unified CLI Tool")
    subparsers = parser.add_subparsers(dest="command")

    # Google Search
    g_parser = subparsers.add_parser("search", help="Perform Google search")
    g_parser.add_argument("query", help="Search query")
    g_parser.add_argument("-n", "--num", type=int, default=5, help="Number of results")

    # Weather
    w_parser = subparsers.add_parser("weather", help="Check weather")
    w_parser.add_argument("city", help="City name")

    # Location
    l_parser = subparsers.add_parser("location", help="Get location info")
    l_parser.add_argument("city", help="City name")

    args = parser.parse_args()

    if args.command == "search":
        google_search(args.query, args.num)
    elif args.command == "weather":
        get_coordinates(args.city) and get_weather(args.city)  #and weather_search
        print("🌤 Weather Report:", get_weather(args.city))
    elif args.command == "location":
        get_coordinates(args.city) , location_search(args.city)
        print("📍 Location Info:", location_search(args.city))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()



