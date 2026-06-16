import pandas as pd

def merge_csv_files(rank_file, features_file, coordinates_file, output_file):
    rank_df = pd.read_csv(rank_file)
    features_df = pd.read_csv(features_file)
    coordinates_df = pd.read_csv(coordinates_file)

    # Keep only required columns from features.csv
    features_df = features_df[
        ["Institute_Name", "NIRF_Rank", "Median_Package_LPA", "Annual_Fees_INR"]
    ]

    # Keep only required columns from coordinates.csv
    coordinates_df = coordinates_df[
        ["Institute_Name", "Latitude", "Longitude", "State"]
    ]

    # Merge
    merged_df = rank_df.merge(features_df, on="Institute_Name", how="left")
    merged_df = merged_df.merge(coordinates_df, on="Institute_Name", how="left")

    merged_df.to_csv(output_file, index=False)
    print(f"Saved: {output_file}")

if __name__ == "__main__":

    from pathlib import Path
    BASE_DIR = Path(__file__).parent
    merge_csv_files(
        "csab_ranks.csv",
        "features.csv",
        "institutes_coordinates.csv",
        "csab_merged.csv"
    )

    merge_csv_files(
        "josaa_ranks.csv",
        "features.csv",
        "institutes_coordinates.csv",
        "josaa_merged.csv"
    )