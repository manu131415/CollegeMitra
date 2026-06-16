import pandas as pd
import requests
import time

INPUT_FILE = "institute_coordinates_retry.csv"
OUTPUT_FILE = "institute_coordinates_final.csv"

SPECIAL_NAMES = {
    "National Institute of Electronics and Information Technology, Agartala": "NIELIT Agartala",
    "National Institute of Electronics and Information Technology, Aizawl": "NIELIT Aizawl",
    "National Institute of Electronics and Information Technology, Ajmer (Rajasthan)": "NIELIT Ajmer",
    "National Institute of Electronics and Information Technology, Aurangabad (Maharashtra)": "NIELIT Aurangabad",
    "National Institute of Electronics and Information Technology, Calicut": "NIELIT Calicut",
    "National Institute of Electronics and Information Technology, Gorakhpur (UP)": "NIELIT Gorakhpur",
    "National Institute of Electronics and Information Technology, Imphal": "NIELIT Imphal",
    "National Institute of Electronics and Information Technology, Kohima": "NIELIT Kohima",
    "National Institute of Electronics and Information Technology, Patna (Bihar)": "NIELIT Patna",
    "National Institute of Electronics and Information Technology, Ropar (Punjab)": "NIELIT Ropar",
    "National Institute of Electronics and Information Technology, Srinagar": "NIELIT Srinagar",
}

MANUAL_COORDS = {
    "Atal Bihari Vajpayee Indian Institute of Information Technology & Management Gwalior": (26.2494, 78.1734),
    "Central University of Jammu": (32.6130, 74.8429),
    "Dr. B R Ambedkar National Institute of Technology, Jalandhar": (31.3959, 75.5352),
    "Indian Institute of Information Technology (IIIT) Nagpur": (21.0273, 79.0317),
    "Indian Institute of Information Technology (IIIT)Kota, Rajasthan": (25.1416, 75.8648),
    "Indian Institute of Information Technology Bhopal": (23.1765, 77.3010),
    "Indian Institute of Information Technology Srirangam, Tiruchirappalli": (10.8613, 78.6928),
    "Indian Institute of Information Technology Tiruchirappalli": (10.8613, 78.6928),
    "Indian Institute of Information Technology Surat": (21.1702, 72.7852),
    "Indian Institute of Information Technology(IIIT) Kilohrad, Sonepat, Haryana": (28.8229, 77.1325),
    "Indian Maritime University - Visakhapatnam Campus": (17.6868, 83.2185),
    "National Institute of Advanced Manufacturing Technology, Ranchi": (23.3441, 85.3096),
    "National Institute of Technical Teachers Training and Research Bhopal": (23.3096, 77.3610),
    "National Institute of Technology Patna": (25.5354, 84.8517),
    "National Institute of Technology Sikkim": (27.2980, 88.5990),
    "Pt. Dwarka Prasad Mishra Indian Institute of Information Technology, Design & Manufacture Jabalpur": (23.1778, 80.0246),
    "Puducherry Technological University, Puducherry": (11.9395, 79.8083),
    "Rajiv Gandhi National Aviation University, Fursatganj, Amethi (UP)": (26.2482, 81.8128),
    "Sant Longowal Institute of Engineering and Technology": (30.1907, 75.6922),
}

HEADERS = {
    "User-Agent": "CollegeMitra/1.0"
}

def geocode(query):
    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": query,
        "format": "jsonv2",
        "limit": 1,
        "countrycodes": "in"
    }

    try:
        r = requests.get(
            url,
            params=params,
            headers=HEADERS,
            timeout=40
        )

        if r.status_code != 200:
            return None

        data = r.json()

        if not data:
            return None

        return (
            float(data[0]["lat"]),
            float(data[0]["lon"])
        )

    except Exception:
        return None


df = pd.read_csv(INPUT_FILE)

for idx, row in df.iterrows():

    if pd.notna(row["Latitude"]) and pd.notna(row["Longitude"]):
        continue

    name = str(row["Institute_Name"]).strip()

    # manual coordinates
    if name in MANUAL_COORDS:
        lat, lon = MANUAL_COORDS[name]

        df.at[idx, "Latitude"] = lat
        df.at[idx, "Longitude"] = lon

        print("✓ manual:", name)
        continue

    if name in SPECIAL_NAMES:
        name = SPECIAL_NAMES[name]

    queries = [
        name,
        f"{name}, India",
        f"{name} campus",
        f"{name} university",
        f"{name} college",
        f"{name} institute",
    ]

    found = False

    for query in queries:

        coords = geocode(query)

        if coords:
            lat, lon = coords

            df.at[idx, "Latitude"] = lat
            df.at[idx, "Longitude"] = lon

            print("✓", row["Institute_Name"])
            found = True
            break

        time.sleep(1.5)

    if not found:
        print("✗", row["Institute_Name"])

df.to_csv(OUTPUT_FILE, index=False)

filled = df["Latitude"].notna().sum()

print("\nSaved:", OUTPUT_FILE)
print(f"Coordinates filled: {filled}/{len(df)}")

missing = df[
    df["Latitude"].isna() |
    df["Longitude"].isna()
]

print("\nRemaining Missing:")
for x in missing["Institute_Name"]:
    print(x)