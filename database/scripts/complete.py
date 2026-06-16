import pandas as pd
import requests
import re
import time
from tqdm import tqdm

INPUT_FILE = "institute_coordinates_filled.csv"
OUTPUT_FILE = "institute_coordinates_completed.csv"

df = pd.read_csv(INPUT_FILE)

HEADERS = {
    "User-Agent": "CollegeMitra/1.0"
}

def clean_name(name):
    name = str(name)

    replacements = {
        "(IIIT)": "",
        "(IIT)": "",
        "(NIT)": "",
        "Andra Pradesh": "Andhra Pradesh",
        "&": "and",
    }

    for old, new in replacements.items():
        name = name.replace(old, new)

    name = re.sub(r"\s+", " ", name)
    return name.strip()

def generate_queries(name):
    name = clean_name(name)

    queries = [
        name,
        f"{name}, India",
        f"{name} campus",
        f"{name} engineering college",
    ]

    # Remove state names if present
    short = re.split(r",", name)[0].strip()

    if short != name:
        queries.append(short)
        queries.append(f"{short}, India")

    return list(dict.fromkeys(queries))

def geocode(query):
    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": query,
        "format": "jsonv2",
        "limit": 1,
        "countrycodes": "in"
    }

    try:
        response = requests.get(
            url,
            params=params,
            headers=HEADERS,
            timeout=20
        )

        if response.status_code != 200:
            return None

        data = response.json()

        if len(data) == 0:
            return None

        return (
            float(data[0]["lat"]),
            float(data[0]["lon"])
        )

    except Exception:
        return None

missing = df[
    df["Latitude"].isna() |
    df["Longitude"].isna()
]

print("Missing institutes:", len(missing))

for idx in tqdm(missing.index):

    institute = df.loc[idx, "Institute_Name"]

    coords = None

    for query in generate_queries(institute):

        coords = geocode(query)

        if coords:
            break

        time.sleep(1.2)

    if coords:
        lat, lon = coords

        df.loc[idx, "Latitude"] = lat
        df.loc[idx, "Longitude"] = lon

        print(f"✓ {institute}")
    else:
        print(f"✗ {institute}")

df.to_csv(OUTPUT_FILE, index=False)

filled = df["Latitude"].notna().sum()

print("\nSaved:", OUTPUT_FILE)
print(f"Coordinates filled: {filled}/{len(df)}")