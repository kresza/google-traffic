import googlemaps
import json
import csv
from datetime import datetime
from urllib.parse import urlparse, parse_qs
import time
import re
from googlemaps import Client
from database import Database
from dotenv import load_dotenv
import os


def get_coordinates_from_url(api_key, url):
    """Get start and end coordinates from a Google Maps URL."""
    gmaps: Client = googlemaps.Client(key=api_key)

    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    print("Parsed URL:", parsed_url)
    print("Query Parameters:", query_params)

    start_location = query_params.get('origin', [''])[0]
    end_location = query_params.get('destination', [''])[0]

    start_coordinates = get_coordinates(gmaps, start_location)
    end_coordinates = get_coordinates(gmaps, end_location)

    return start_coordinates, end_coordinates


def get_coordinates(gmaps, location):
    """Get coordinates (latitude, longitude) for a given location using Google Maps API."""
    try:
        geocode_result = gmaps.geocode(location)
        if not geocode_result:
            print(f"No results found for location: {location}")
            return None

        return geocode_result[0]['geometry']['location']
    except Exception as e:
        print(f"Failed to get coordinates for location: {location}")
        print(f"Error: {e}")
        return None


def calculate_route(api_key, start_coordinates, end_coordinates, routName):
    try:
        gmaps = googlemaps.Client(key=api_key)

        print("Calculating routes...")

        directions_results = gmaps.directions(
            start_coordinates,
            end_coordinates,
            mode="driving",
            departure_time=datetime.now(),
            alternatives=True,
        )
        # FIND SHORTEST ROUTE
        shortest_route = min(directions_results, key=lambda x: x['legs'][0]['distance']['value'])

        print("API Response:", shortest_route)

        duration_in_traffic = shortest_route['legs'][0]['duration_in_traffic']['text']
        minute = int(re.search(r'(\d+) min', duration_in_traffic).group(1))
        origin = shortest_route['legs'][0]['start_address'].strip('"')
        destination = shortest_route['legs'][0]['end_address'].strip('"')
        distance = shortest_route['legs'][0]['distance']['text'].replace(' km', '')

        day_of_week = datetime.today().weekday()
        date = datetime.today().strftime('%Y.%m.%d')
        time_of_day = datetime.now().strftime("%H:%M")

        print(f"Route calculated. Waiting for 2 seconds...")
        time.sleep(2)

        # CSV file
        with open('route_times.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow([date, day_of_week, time_of_day, routName, distance, minute])
            # save to csv in order -> date, dayofweek 0-monday 6-sunday, routName , travel time in minutes

        print(f"Origin: {origin}")
        print(f"Destination: {destination}")
        print(f"Distance: {distance} km")
        print(f"Duration in traffic: {duration_in_traffic}")

    except Exception as e:
        print(f"Error calculating route: {e}")


if __name__ == "__main__":
    load_dotenv(dotenv_path='connection.env')
    api_key = os.getenv('API_KEY', default='')

    if not api_key:
        print("API key not found. Check the connection.env file.")
    else:
        print("API key has been found")
        google_maps_url = 'https://www.google.com/maps/dir/?api=1&origin=Pasaż+Grunwaldzki+Wrocław&destination=Bielany+Wrocławskie+Wrocław&travelmode=driving'  # route url
        start_coordinates, end_coordinates = get_coordinates_from_url(api_key, google_maps_url)
        routName = 'BIELPASAZ'
        i = 0
        nu_records = 5  # how many records

        while i < nu_records:
            calculate_route(api_key, start_coordinates, end_coordinates, routName)
            i = i + 1
            print('--------------------------------')
            print('records iteration', i, 'to', nu_records)
            print('--------------------------------')
            time.sleep(5)







