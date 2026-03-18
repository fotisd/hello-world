#!/usr/bin/env python3
"""
Google Maps Top Places Finder

Finds the top-rated restaurants, hotels, bars, and sights in a given city,
filtered by minimum review count and sorted by rating.
"""

import argparse
import os
import sys
import time

import googlemaps
from tabulate import tabulate

CATEGORIES = {
    "restaurants": {
        "type": "restaurant",
        "keyword": "restaurant",
        "min_reviews": 200,
        "top_n": 15,
    },
    "hotels": {
        "type": "lodging",
        "keyword": "hotel",
        "min_reviews": 200,
        "top_n": 15,
    },
    "bars": {
        "type": "bar",
        "keyword": "bar",
        "min_reviews": 200,
        "top_n": 15,
    },
    "sights": {
        "type": "tourist_attraction",
        "keyword": "tourist attraction",
        "min_reviews": 0,
        "top_n": 15,
    },
}


def get_city_location(client, city_name):
    """Geocode a city name to lat/lng coordinates."""
    results = client.geocode(city_name)
    if not results:
        print(f"Error: Could not find city '{city_name}'.")
        sys.exit(1)
    location = results[0]["geometry"]["location"]
    formatted = results[0]["formatted_address"]
    return location, formatted


def search_places(client, location, category_config):
    """Search for places using Text Search to gather enough candidates."""
    places = {}
    place_type = category_config["type"]
    keyword = category_config["keyword"]

    # Use nearby search with rankby prominence for well-reviewed places
    next_page_token = None
    for _ in range(3):  # Up to 3 pages (60 results max)
        params = {
            "location": (location["lat"], location["lng"]),
            "radius": 15000,
            "type": place_type,
            "keyword": keyword,
        }
        if next_page_token:
            params = {"page_token": next_page_token}

        response = client.places_nearby(**params)
        results = response.get("results", [])

        for place in results:
            place_id = place.get("place_id")
            if place_id and place_id not in places:
                places[place_id] = {
                    "name": place.get("name", "N/A"),
                    "rating": place.get("rating", 0),
                    "reviews": place.get("user_ratings_total", 0),
                    "address": place.get("vicinity", "N/A"),
                    "place_id": place_id,
                }

        next_page_token = response.get("next_page_token")
        if not next_page_token:
            break
        # Google requires a short delay before using next_page_token
        time.sleep(2)

    return places


def filter_and_rank(places, min_reviews, top_n):
    """Filter by minimum reviews and return top N sorted by rating."""
    filtered = [p for p in places.values() if p["reviews"] >= min_reviews]
    filtered.sort(key=lambda x: (-x["rating"], -x["reviews"]))
    return filtered[:top_n]


def display_results(category_name, places):
    """Display results as a formatted table."""
    if not places:
        print(f"\n{'=' * 60}")
        print(f"  TOP {category_name.upper()} — No results found matching criteria")
        print(f"{'=' * 60}")
        return

    print(f"\n{'=' * 60}")
    print(f"  TOP {len(places)} {category_name.upper()}")
    print(f"{'=' * 60}")

    table_data = []
    for rank, place in enumerate(places, 1):
        table_data.append([
            rank,
            place["name"],
            f"{place['rating']:.1f}",
            f"{place['reviews']:,}",
            place["address"][:50],
        ])

    headers = ["#", "Name", "Rating", "Reviews", "Address"]
    print(tabulate(table_data, headers=headers, tablefmt="rounded_grid"))


def main():
    parser = argparse.ArgumentParser(
        description="Find top-rated places in any city using Google Maps."
    )
    parser.add_argument(
        "city",
        help="City name to search (e.g., 'Paris', 'New York', 'Tokyo')",
    )
    parser.add_argument(
        "--api-key",
        default=os.environ.get("GOOGLE_MAPS_API_KEY"),
        help="Google Maps API key (or set GOOGLE_MAPS_API_KEY env var)",
    )
    parser.add_argument(
        "--categories",
        nargs="+",
        choices=list(CATEGORIES.keys()),
        default=list(CATEGORIES.keys()),
        help="Categories to search (default: all)",
    )
    parser.add_argument(
        "--radius",
        type=int,
        default=15000,
        help="Search radius in meters (default: 15000)",
    )

    args = parser.parse_args()

    if not args.api_key:
        print("Error: Google Maps API key is required.")
        print("Set it via --api-key flag or GOOGLE_MAPS_API_KEY environment variable.")
        print()
        print("To get an API key:")
        print("  1. Go to https://console.cloud.google.com/")
        print("  2. Enable the 'Places API' and 'Geocoding API'")
        print("  3. Create an API key under 'Credentials'")
        sys.exit(1)

    client = googlemaps.Client(key=args.api_key)

    # Resolve city to coordinates
    location, formatted_address = get_city_location(client, args.city)
    print(f"\nSearching in: {formatted_address}")
    print(f"Coordinates: {location['lat']:.4f}, {location['lng']:.4f}")

    # Search each category
    for category_name in args.categories:
        config = CATEGORIES[category_name].copy()
        print(f"\nSearching for top {category_name}...")

        places = search_places(client, location, config)
        top_places = filter_and_rank(places, config["min_reviews"], config["top_n"])
        display_results(category_name, top_places)


if __name__ == "__main__":
    main()
