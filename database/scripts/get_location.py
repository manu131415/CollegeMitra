import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from tqdm import tqdm
import time

INPUT_FILE = "institute_coordinates.csv"
OUTPUT_FILE = "institute_coordinates_filled.csv"

# Load CSV
df = pd.read_csv(INPUT_FILE)

# Detect column names
name_col = "Institute_Name"
lat_col = "Latitude"
lon_col = "Longitude"

if name_col not in df.columns:
    raise ValueError(
        f"Column '{name_col}' not found. Available columns: {list(df.columns)}"
    )

# Create latitude/longitude columns if missing
if lat_col not in df.columns:
    df[lat_col] = None

if lon_col not in df.columns:
    df[lon_col] = None

# Geocoder
geolocator = Nominatim(user_agent="college_coordinates_filler")
geocode = RateLimiter(
    geolocator.geocode,
    min_delay_seconds=1.1,
    max_retries=3,
    error_wait_seconds=5
)

# Cache to avoid repeated lookups
cache = {}

for idx in tqdm(df.index, desc="Geocoding institutes"):
    # Skip rows that already have coordinates
    if pd.notna(df.at[idx, lat_col]) and pd.notna(df.at[idx, lon_col]):
        continue

    institute = str(df.at[idx, name_col]).strip()

    if not institute:
        continue

    if institute in cache:
        lat, lon = cache[institute]
        df.at[idx, lat_col] = lat
        df.at[idx, lon_col] = lon
        continue

    try:
        # Add India for better accuracy
        query = f"{institute}, India"

        location = geocode(query)

        if location:
            lat = location.latitude
            lon = location.longitude

            df.at[idx, lat_col] = lat
            df.at[idx, lon_col] = lon

            cache[institute] = (lat, lon)

            print(f"✓ {institute}")
        else:
            print(f"✗ Not found: {institute}")

    except Exception as e:
        print(f"Error for {institute}: {e}")

    # Be polite to the free API
    time.sleep(0.1)

# Save result
df.to_csv(OUTPUT_FILE, index=False)

print("\nDone!")
print(f"Saved to: {OUTPUT_FILE}")

filled = df[lat_col].notna().sum()
total = len(df)

print(f"Coordinates filled: {filled}/{total}")