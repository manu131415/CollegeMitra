import pandas as pd

df = pd.read_csv("institute_coordinates_final.csv")

missing = df[
    df["Latitude"].isna() |
    df["Longitude"].isna()
]

print("Missing:", len(missing))

missing["Institute_Name"].to_csv(
    "missing_institutes.csv",
    index=False
)