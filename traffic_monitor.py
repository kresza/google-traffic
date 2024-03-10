import googlemaps
import json
import csv
from datetime import datetime
from urllib.parse import urlparse, parse_qs
import time
import re
from googlemaps import Client


def get_coordinates_from_url(api_key, url):
    """Get start and end coordinates from a Google Maps URL."""
    gmaps: Client = googlemaps.Client(key=api_key)

    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    print("Parsed URL:", parsed_url)
    print("Query Parameters:", query_params)

    start_location = query_params.get('saddr', [''])[0]
    end_location = query_params.get('daddr', [''])[0]

    start_coordinates = get_coordinates(gmaps, start_location)
    end_coordinates = get_coordinates(gmaps, end_location)

    return start_coordinates, end_coordinates


def get_coordinates(gmaps, location):
    """Get coordinates (latitude, longitude) for a given location using Google Maps API."""
    try:
        geocode_result = gmaps.geocode(location)
        if not geocode_result:
            raise Exception(f"No results found for location: {location}")
        return geocode_result[0]['geometry']['location']
    except Exception as e:
        print(f"Failed to get coordinates for location: {location}")
        print(f"Error: {e}")
        return None


def calculate_route(api_key, route_url, log_response=False):
    try:
        gmaps = googlemaps.Client(key=api_key)

        start_coordinates = (51.11160771021999, 17.06008851512044)  #Replace with actual start coordinates 51.11245993415498, 17.055864466280198
        end_coordinates = (51.0352209, 16.9678799)
        start_place = 'PasazGrunwaldzki'
        end_place = 'BielanyWroclawskie'

        print("Calculating route...")

        directions_result = gmaps.directions(
            start_coordinates,
            end_coordinates,
            mode="driving",
            departure_time=datetime.now(),
        )
        print("API Response:", directions_result)
        if log_response:
            with open('response.tmp.txt', 'w') as outfile:
                outfile.write(json.dumps(directions_result, indent=2))

        duration_in_traffic = directions_result[0]['legs'][0]['duration_in_traffic']['text']
        minutes = int(re.search(r'(\d+) min', duration_in_traffic).group(1))

        day_of_week = datetime.today().weekday()
        date = datetime.today().strftime('%Y.%m.%d')
        time_of_day = datetime.now().strftime("%H:%M")

        print(f"Route calculated. Waiting for 2 seconds...")
        time.sleep(2)

        # Save the route data to a CSV file
        with open('route_times.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([date,day_of_week, time_of_day, start_place, end_place, minutes])
            # save to csv in order -> date, dayofweek 0-monday 6-sunday, start place, end place, travel time in minutes

        print(f"Duration in traffic: {duration_in_traffic}")

    except Exception as e:
        print(f"Error calculating route: {e}")


if __name__ == "__main__":
    api_key = "AIzaSyDjArNix8I0akx1uouwhcAO3743fLT6ncE"

    # Replace 'YOUR_GOOGLE_MAPS_URL' with your actual Google Maps URL
    google_maps_url = 'https://maps.app.goo.gl/V75gsHxx1otxYxoT9'

    i = 0
    nu_records = 5  # how many records
    # Run the function
    while i < nu_records:
        calculate_route(api_key, google_maps_url)
        i = i + 1
        print('--------------------------------')
        print('records iteration', i, 'to', nu_records)
        print('--------------------------------')



