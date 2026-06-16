import pandas as pd
import requests
import time

INPUT_FILE = "institute_coordinates_retry.csv"
OUTPUT_FILE = "institute_coordinates_retry.csv"

df = pd.read_csv(INPUT_FILE)

SPECIAL_NAMES = {
    "Indian Institute of Crop Processing Technology, Thanjavur, Tamilnadu":
        "Indian Institute of Food Processing Technology Thanjavur",

    "lndian Institute of Food Processing Technology, Thanjavur, Tamil Naidu.":
        "Indian Institute of Food Processing Technology Thanjavur",

    "Indian Institute of Technology (ISM) Dhanbad":
        "IIT ISM Dhanbad",

    "Indian School of Mines Dhanbad":
        "IIT ISM Dhanbad",

    "Dr. B R Ambedkar National Institute of Technology, Jalandhar":
        "NIT Jalandhar",

    "Malaviya National Institute of Technology Jaipur":
        "MNIT Jaipur",

    "Maulana Azad National Institute of Technology Bhopal":
        "MANIT Bhopal",

    "Indian Institute of Information Technology (IIIT) Nagpur":
        "IIIT Nagpur",

    "Indian Institute of Information Technology (IIIT) Ranchi":
        "IIIT Ranchi",

    "Indian Institute of Information Technology Bhagalpur":
        "IIIT Bhagalpur",

    "Indian Institute of Information Technology Bhopal":
        "IIIT Bhopal",

    "Indian Institute of Information Technology Surat":
        "IIIT Surat",

    "Indian Institute of Information Technology Tiruchirappalli":
        "IIIT Tiruchirappalli",

    "Indian Institute of Information Technology Manipur":
        "IIIT Manipur",

    "Indian Institute of Information Technology(IIIT)Kota, Rajasthan":
        "IIIT Kota",

    "Indian Institute of Information Technology(IIIT) Kottayam":
        "IIIT Kottayam",

    "Indian Institute of Information Technology(IIIT) Una, Himachal Pradesh":
        "IIIT Una",

    "Indian Institute of Information Technology(IIIT) Dharwad":
        "IIIT Dharwad",

    "Indian Institute of Information Technology(IIIT) Kalyani, West Bengal":
        "IIIT Kalyani",

    "Indian Institute of Information Technology(IIIT) Kilohrad, Sonepat, Haryana":
        "IIIT Sonepat",

    "Indian Institute of Technology Gandhinagar":
        "IIT Gandhinagar"
}

SPECIAL_NAMES.update({

    "Atal Bihari Vajpayee Indian Institute of Information Technology & Management Gwalior":
        "ABV-IIITM Gwalior",

    "Central University of Jammu":
        "Central University of Jammu Samba",

    "Central institute of Technology Kokrajar, Assam":
        "CIT Kokrajhar",

    "Chhattisgarh Swami Vivekanada Technical University, Bhilai (CSVTU Bhilai)":
        "CSVTU Bhilai",

    "INDIAN INSTITUTE OF INFORMATION TECHNOLOGY SENAPATI MANIPUR":
        "IIIT Manipur",

    "Indian Institute of Carpet Technology, Bhadohi":
        "Bhadohi Uttar Pradesh",

    "Indian Institute of Engineering Science and Technology, Shibpur":
        "IIEST Shibpur",

    "Indian Institute of Handloom Technology(IIHT), Varanasi":
        "IIHT Varanasi",

    "Indian Institute of Handloom Technology, Salem":
        "IIHT Salem",

    "Indian Maritime University - Visakhapatnam Campus":
        "Indian Maritime University Visakhapatnam",

    "Islamic University of Science and Technology Kashmir":
        "Islamic University of Science and Technology Awantipora",

    "National Institute of Advanced Manufacturing Technology, Ranchi":
        "NIAMT Ranchi",

    "National Institute of Food Technology Entrepreneurship and Management, Kundli":
        "NIFTEM Kundli",

    "National Institute of Food Technology Entrepreneurship and Management, Sonepat, Haryana":
        "NIFTEM Kundli",

    "National Institute of Food Technology Entrepreneurship and Management, Thanjavur":
        "NIFTEM Thanjavur",

    "National Institute of Food Technology, Entrepreneurship and Management (NIFTEM) - Thanjavur":
        "NIFTEM Thanjavur",

    "National Institute of Foundry & Forge Technology, Hatia, Ranchi":
        "NIFFT Ranchi",

    "National Institute of Technical Teachers Training and Research Bhopal":
        "NITTTR Bhopal",

    "North Eastern Regional Institute of Science and Technology, Nirjuli-791109 (Itanagar),Arunachal Pradesh":
        "NERIST Nirjuli",

    "Pt. Dwarka Prasad Mishra Indian Institute of Information Technology, Design & Manufacture Jabalpur":
        "PDPM IIITDM Jabalpur",

    "Puducherry Technological University, Puducherry":
        "Puducherry Technological University",

    "Rajiv Gandhi National Aviation University, Fursatganj, Amethi (UP)":
        "Rajiv Gandhi National Aviation University",

    "Sant Longowal Institute of Engineering and Technology":
        "SLIET Longowal",

    "School of Studies of Engineering and Technology, Guru Ghasidas Vishwavidyalaya, Bilaspur":
        "Guru Ghasidas Vishwavidyalaya Bilaspur",

    "Shri G. S. Institute of Technology and Science Indore":
        "SGSITS Indore",

    "National Institute of Technology Nagaland":
        "NIT Nagaland",

    "National Institute of Technology Patna":
        "NIT Patna",

    "National Institute of Technology Raipur":
        "NIT Raipur",

    "National Institute of Technology Sikkim":
        "NIT Sikkim",

})

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

    except:
        return None


for idx, row in df.iterrows():

    if pd.notna(row["Latitude"]) and pd.notna(row["Longitude"]):
        continue

    name = str(row["Institute_Name"]).strip()

    if name in SPECIAL_NAMES:
        name = SPECIAL_NAMES[name]

    # queries = [
    #     name,
    #     f"{name}, India",
    #     f"{name} campus",
    #     f"{name} engineering college",
    #     f"{name} university"
    # ]
    
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

print(f"\nFilled {df['Latitude'].notna().sum()}/{len(df)}")