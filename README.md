# Google Maps Top Places Finder

Find the top-rated restaurants, hotels, bars, and sights in any city using the Google Maps Places API.

## Features

- **Top 15 Restaurants** — filtered to places with at least 200 reviews
- **Top 15 Hotels** — filtered to places with at least 200 reviews
- **Top 15 Bars** — filtered to places with at least 200 reviews
- **Top 15 Sights** — top tourist attractions
- Results sorted by rating, then by number of reviews
- Configurable search radius and category selection

## Prerequisites

1. A Google Maps API key with the following APIs enabled:
   - **Places API**
   - **Geocoding API**
2. Python 3.8+

### Getting an API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select an existing one)
3. Enable the **Places API** and **Geocoding API**
4. Go to **Credentials** and create an API key

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
# Set your API key
export GOOGLE_MAPS_API_KEY="your-api-key-here"

# Search all categories in a city
python top_places.py "Paris"

# Search a specific city with the key as an argument
python top_places.py "New York" --api-key YOUR_API_KEY

# Search only specific categories
python top_places.py "Tokyo" --categories restaurants bars

# Custom search radius (in meters)
python top_places.py "London" --radius 20000
```

### Available Categories

| Category      | Type               | Min Reviews |
|---------------|--------------------|-------------|
| `restaurants` | Restaurants        | 200         |
| `hotels`      | Hotels / Lodging   | 200         |
| `bars`        | Bars               | 200         |
| `sights`      | Tourist Attractions| 0           |

## Example Output

```
Searching in: Paris, France
Coordinates: 48.8566, 2.3522

Searching for top restaurants...

============================================================
  TOP 15 RESTAURANTS
============================================================
╭─────┬──────────────────────────┬──────────┬───────────┬──────────────────────╮
│   # │ Name                     │ Rating   │ Reviews   │ Address              │
├─────┼──────────────────────────┼──────────┼───────────┼──────────────────────┤
│   1 │ Le Jules Verne           │ 4.5      │ 5,432     │ Av. Gustave Eiffel   │
│   2 │ ...                      │ ...      │ ...       │ ...                  │
╰─────┴──────────────────────────┴──────────┴───────────┴──────────────────────╯
```
