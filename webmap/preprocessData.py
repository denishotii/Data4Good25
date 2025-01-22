import pandas as pd
import numpy as np
import json
from fuzzywuzzy import process
from geopy.distance import geodesic

# Load original data
df = pd.read_csv('data/Data4Good_Arolsen_Archives_50k.csv')

# Ensure values are strings and clean Geo Location
df["Geo Location"] = df["Geo Location"].astype(str).apply(lambda x: x.replace('""', '"').strip('"').strip("'"))

# Extract cluster information
def extract_cluster_info(json_data, cluster_to_city):
    try:
        data = json.loads(json_data)
        for marker in data.get("markers", []):
            if "location" in marker and "label" in marker:
                lat, lon = marker["location"]["lat"], marker["location"]["lon"]
                city = marker["label"]
                cluster_id = (lat, lon)
                if cluster_id not in cluster_to_city:
                    cluster_to_city[cluster_id] = {"city": city, "lat": lat, "lon": lon}
    except json.JSONDecodeError:
        pass

# Create mapping
cluster_to_city = {}
df["Geo Location"].dropna().apply(lambda x: extract_cluster_info(x, cluster_to_city))
city_location_mapping = {data["city"]: {"lat": lat, "lon": lon} for (lat, lon), data in cluster_to_city.items()}

# Convert Birthdate to Year, Month, Day
def split_birthdate(date):
    if date.startswith('//'):
        return date[2:], np.nan, np.nan  
    parts = date.split('/')
    if len(parts) == 3:
        return parts[2], parts[1], parts[0]  
    elif len(parts) == 1 and date.isdigit() and len(date) == 4:
        return date, np.nan, np.nan  
    else:
        return None, None, None  

df[['Birth_Year', 'Birth_Month', 'Birth_Day']] = df['Birthdate (Geb)'].apply(lambda x: pd.Series(split_birthdate(str(x))))
df.drop(columns=['Birthdate (Geb)', 'Alternative_Birthdate'], inplace=True)

# Clean Nationality
df["Nationality"] = df["Nationality"].str.lower().str.strip().replace({"stateless": np.nan})

# Apply fuzzy matching
valid_nationalities = ["german", "french", "hungarian", "polish", "austrian", "italian", "czech"]
def fuzzy_correct(nationality):
    if pd.isna(nationality):
        return "unknown"
    match, score = process.extractOne(nationality, valid_nationalities)
    return match if score > 85 else "unknown"

df["Nationality_Corrected"] = df["Nationality"].apply(fuzzy_correct)
df.drop(columns=["Nationality"], inplace=True)

# Save cleaned data
df.to_csv('data/cleaned_holocaust_data.csv', index=False)
print("✅ Cleaned data saved!")
