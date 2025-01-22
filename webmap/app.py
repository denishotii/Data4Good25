import pandas as pd
import numpy as np
import shap
import xgboost as xgb
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import json
import folium
import random
from geopy.distance import geodesic
from fuzzywuzzy import process

df = pd.read_csv('data/Data4Good_Arolsen_Archives_50k.csv')
# df = df.sample(n=3000, random_state=42).reset_index(drop=True)
df_init = df.copy()

# Ensure all values are strings and replace double double-quotes
df["Geo Location"] = df["Geo Location"].astype(str).apply(lambda x: x.replace('""', '"'))
# Ensure values are strings and remove surrounding quotes
df["Geo Location"] = df["Geo Location"].astype(str).apply(lambda x: x.strip('"'))
# Ensure values are strings and remove surrounding single and double quotes
df["Geo Location"] = df["Geo Location"].astype(str).apply(lambda x: x.strip("'").strip('"'))

df_init["Geo Location"] = df["Geo Location"].astype(str).apply(lambda x: x.replace('""', '"'))
df_init["Geo Location"] = df["Geo Location"].astype(str).apply(lambda x: x.strip('"'))
df_init["Geo Location"] = df["Geo Location"].astype(str).apply(lambda x: x.strip("'").strip('"'))


# Dictionary to store cluster to city mappings
cluster_to_city = {}

# Function to extract cluster information from JSON
def extract_cluster_info(json_data):
    try:
        data = json.loads(json_data)  # Parse JSON
        for marker in data.get("markers", []):
            if "location" in marker and "label" in marker:
                lat, lon = marker["location"]["lat"], marker["location"]["lon"]
                city = marker["label"]
                cluster_id = (lat, lon)  # Use lat/lon as a unique cluster key
                if cluster_id not in cluster_to_city:
                    cluster_to_city[cluster_id] = {"city": city, "lat": lat, "lon": lon}
    except json.JSONDecodeError:
        pass  # Skip invalid JSON

# Apply function to extract data
df["Geo Location"].dropna().apply(extract_cluster_info)

# Convert cluster_to_city mapping to the desired format
structured_mapping = {data["city"]: {"lat": lat, "lon": lon} for (lat, lon), data in cluster_to_city.items()}

# Print the structured mapping
# print(json.dumps(structured_mapping, indent=4))

# Optionally, save it as a dictionary for use in predictions
city_location_mapping = structured_mapping

df = df.drop(columns=["Unnamed: 0", "Last_Name", "First Name", "TD", "Alternative Name", "Father (Vater - Eltern)", "Mother (Mutter - Eltern)", "Spouse (Ehem/Ehefr)", "Upper", "Middle", "Volunteers' Comment", "Overall Confidence OCR", "Alternative Nationality 2", "Alternative Nationality 1"])

# Convert to string to avoid errors
df['Birthdate (Geb)'] = df['Birthdate (Geb)'].astype(str)

# Function to split birthdate into components
def split_birthdate(date):
    if date.startswith('//'):  # Case: Birthdate starts with "//"
        return date[2:], np.nan, np.nan  # Extract year, set Month and Day to 0
    
    parts = date.split('/')
    
    if len(parts) == 3:  # Full date case (DD/MM/YYYY)
        return parts[2], parts[1], parts[0]  # Year, Month, Day
    elif len(parts) == 1 and date.isdigit() and len(date) == 4:  # Year only (YYYY)
        return date, np.nan, np.nan  # Set Month and Day to 0
    else:
        return None, None, None  # Handle missing or invalid values

# Apply function to create new columns
df[['Birth_Year', 'Birth_Month', 'Birth_Day']] = df['Birthdate (Geb)'].apply(lambda x: pd.Series(split_birthdate(x)))

# Convert numeric columns to integers where possible
df['Birth_Year'] = pd.to_numeric(df['Birth_Year'], errors='coerce')
df['Birth_Month'] = pd.to_numeric(df['Birth_Month'], errors='coerce')
df['Birth_Day'] = pd.to_numeric(df['Birth_Day'], errors='coerce')

df['Birth_Month'] = np.where(df['Birth_Month'] > 12, np.nan, df['Birth_Month'])
df['Birth_Day'] = np.where(df['Birth_Day'] > 31, np.nan, df['Birth_Day'])    

df['Birth_Year'] = np.where(df['Birth_Year'] < 1800, np.nan, df['Birth_Year'])
df['Birth_Year'] = np.where(df['Birth_Year'] > 1945, np.nan, df['Birth_Year'])

df.drop(columns=['Birthdate (Geb)', 'Alternative_Birthdate'], inplace=True)

df['Religion'] = df['Religion'].replace({
    'Orthodox Christian Christian Christian Christian Christian': 'Orthodox Christian'
})

# Group rare religions
min_count = 5  # Threshold for rare categories
religion_counts = df['Religion'].value_counts()
rare_religions = religion_counts[religion_counts < min_count].index
df['Religion'] = df['Religion'].replace(rare_religions, 'Other')

df = pd.get_dummies(df, columns=['Religion'], prefix='Religion')
print(df.columns)

# Convert boolean columns to integers
religion_columns = [col for col in df.columns if col.startswith('Religion_')]
df[religion_columns] = df[religion_columns].astype(int)

df['Automatic Validation'].isna().sum()
df['Automatic Validation'] = df['Automatic Validation'].fillna('Unknown')


df["Nationality"] = df["Nationality"].str.replace(r"(?i)\bFormerly\b", "", regex=True).str.strip()

df["Nationality"] = df["Nationality"].str.lower().replace(r"stateless", np.nan, regex=True)


# Convert valid nationalities list to lowercase
valid_nationalities = [
    # Common nationalities (ISO 3166)
    "afghan", "albanian", "algerian", "american", "andorran", "angolan", "argentine", "armenian", "australian", "austrian",
    "azerbaijani", "bahamian", "bahraini", "bangladeshi", "barbadian", "belarusian", "belgian", "belizean", "beninese", "bhutanese",
    "bolivian", "bosnian", "botswanan", "brazilian", "british", "bruneian", "bulgarian", "burkinabé", "burmese", "burundian",
    "cambodian", "cameroonian", "canadian", "cape verdean", "central african", "chadian", "chilean", "chinese", "colombian",
    "comoran", "congolese", "costa rican", "croatian", "cuban", "cypriot", "czech", "danish", "djiboutian", "dominican",
    "dutch", "east timorese", "ecuadorean", "egyptian", "emirati", "equatorial guinean", "eritrean", "estonian", "eswatini",
    "ethiopian", "fijian", "finnish", "french", "gabonese", "gambian", "georgian", "german", "ghanaian", "greek",
    "grenadian", "guatemalan", "guinean", "guyanese", "haitian", "honduran", "hungarian", "icelandic", "indian", "indonesian",
    "iranian", "iraqi", "irish", "israeli", "italian", "ivorian", "jamaican", "japanese", "jordanian", "kazakh",
    "kenyan", "kiribati", "kuwaiti", "kyrgyz", "lao", "latvian", "lebanese", "lesotho", "liberian", "libyan",
    "liechtensteiner", "lithuanian", "luxembourgish", "macedonian", "malagasy", "malawian", "malaysian", "maldivian",
    "malian", "maltese", "marshallese", "mauritanian", "mauritian", "mexican", "micronesian", "moldovan", "monacan",
    "mongolian", "montenegrin", "moroccan", "mozambican", "myanmar", "namibian", "nauruan", "nepalese", "new zealander",
    "nicaraguan", "nigerian", "north korean", "norwegian", "omani", "pakistani", "palauan", "palestinian", "panamanian",
    "papua new guinean", "paraguayan", "peruvian", "philippine", "polish", "portuguese", "qatari", "romanian", "russian",
    "rwandan", "saint lucian", "salvadoran", "samoan", "saudi", "scottish", "senegalese", "serbian", "seychellois",
    "sierra leonean", "singaporean", "slovak", "slovenian", "solomon islander", "somali", "south african", "south korean",
    "south sudanese", "spanish", "sri lankan", "sudanese", "surinamese", "swedish", "swiss", "syrian", "taiwanese",
    "tajik", "tanzanian", "thai", "togolese", "tongan", "trinidadian", "tunisian", "turkish", "turkmen", "tuvaluan",
    "ugandan", "ukrainian", "uruguayan", "uzbek", "venezuelan", "vietnamese", "welsh", "yemeni", "zambian", "zimbabwean",

    # Historical nationalities
    "austro-hungarian", "prussian", "bohemian", "ottoman", "soviet", "yugoslav", "czechoslovak", "west german", "east german",
    "rhodesian", "serbo-croatian", "mandarin", "manchu", "ming", "byzantine",

    # Stateless or refugee identities
    "stateless", "refugee", "displaced", "unknown",

    # Manually added for necessity
    "yugoslavian", "ussr"
]

# Manual correction mapping for specific cases
manual_corrections = {
    "argentinian": "argentine",
    "luxembourger": "luxembourgish",
    "germna": "german",  # Common OCR mistake
    "polan": "polish"  # Common OCR mistake
}

# Convert all nationalities in data to lowercase and strip spaces
df["Nationality"] = df["Nationality"].str.lower().str.strip()

# Apply manual corrections first
df["Nationality_Corrected"] = df["Nationality"].replace(manual_corrections)

# Fuzzy matching function for remaining uncorrected values
def fuzzy_correct(nationality):
    if pd.isna(nationality):  # Skip NaN values
        return None
    match, score = process.extractOne(nationality, valid_nationalities)
    return match if score > 85 else nationality  # Keep original if match is weak


# Apply fuzzy matching for remaining uncorrected values
df["Nationality_Corrected"] = df["Nationality_Corrected"].apply(fuzzy_correct)

# Identify cases where fuzzy matching changed the nationality
data_fuzzy_changed = df[df["Nationality"] != df["Nationality_Corrected"]]

# Print fuzzy-matched values
# print("Fuzzy-matched corrections:")
# print(data_fuzzy_changed[["Nationality", "Nationality_Corrected"]])

# Identify remaining unrecognized nationalities
unrecognized = df[~df["Nationality_Corrected"].isin(valid_nationalities)]
# print("\nRemaining Unrecognized Nationalities:")
# print(unrecognized["Nationality_Corrected"].unique())

# Find nationalities not in the valid list
valid_nationalities.append(None)
data_unrecognized = df[~df["Nationality_Corrected"].isin(valid_nationalities)]
# Show the indexes and the unrecognized nationalities
df = df[~df["Nationality_Corrected"].isin(data_unrecognized['Nationality_Corrected'])].reset_index(drop=True)

df.drop(columns=['Nationality', 'Inferred Nationality'], inplace=True)

# Fill None values with "unknown"
df["Nationality_Corrected"] = df["Nationality_Corrected"].fillna("unknown")

# Apply Label Encoding
label_encoder = LabelEncoder()
df["Nationality_Corrected_Encoded"] = label_encoder.fit_transform(df["Nationality_Corrected"])

df.drop(columns=['Nationality_Corrected'], inplace=True)

# Impute missing values with the mean of each column
df["Birth_Year"].fillna(df["Birth_Year"].mean(), inplace=True)
df["Birth_Month"].fillna(df["Birth_Month"].mean(), inplace=True)
df["Birth_Day"].fillna(df["Birth_Day"].mean(), inplace=True)

# Convert Birth_Year to integer (optional if you don't want decimals)
df["Birth_Year"] = df["Birth_Year"].round().astype(int)
df["Birth_Month"] = df["Birth_Month"].round().astype(int)
df["Birth_Day"] = df["Birth_Day"].round().astype(int)

# Define a mapping to ensure a consistent order
validation_mapping = {
    "Unknown": 4,
    "Matched": 3,
    "Above threshold for Last Name and TD": 2,
    "To be validated": 1,
    "Submitted": 0
}

# Apply mapping to encode the column
df["Automatic_Validation_Encoded"] = df["Automatic Validation"].map(validation_mapping).round().astype(int)
df.drop(columns=['Automatic Validation'], inplace=True)

# Assign DBSCAN and K-Means cluster labels to df['Geo Location']

# Function to assign DBSCAN clusters to each person's locations
def assign_dbscan_clusters(json_data, dbscan_clusters, geo_array):
    try:
        data = json.loads(json_data)  # Parse JSON
        clusters = []
        for marker in data.get("markers", []):
            if "location" in marker:
                lat, lon = marker["location"]["lat"], marker["location"]["lon"]
                idx = np.where((geo_array == [lat, lon]).all(axis=1))[0]
                if len(idx) > 0:
                    clusters.append(dbscan_clusters[idx[0]])
                else:
                    clusters.append(-1)  # Noise point
        return clusters
    except json.JSONDecodeError:
        return []

# Function to assign K-Means clusters to each person's locations
def assign_kmeans_clusters(json_data, kmeans, geo_array):
    try:
        data = json.loads(json_data)  # Parse JSON
        clusters = []
        for marker in data.get("markers", []):
            if "location" in marker:
                lat, lon = marker["location"]["lat"], marker["location"]["lon"]
                clusters.append(kmeans.predict([[lat, lon]])[0])
        return clusters
    except json.JSONDecodeError:
        return []


# Assign K-Means clusters
df["KMeans_Clusters"] = df["Geo Location"].apply(lambda x: assign_kmeans_clusters(x, kmeans, geo_array))
df.drop(columns=['Geo Location', 'Birth Place'], inplace=True)


# Determine the maximum number of clusters any person has
max_stops = df["KMeans_Clusters"].apply(len).max()

# Set a reasonable maximum number of cluster columns
max_columns = min(max_stops, 10)  # Limit to 10 columns, even if max_stops > 10

# Create columns for each cluster (up to max_columns)
for i in range(max_columns):
    df[f"Cluster_{i+1}"] = df["KMeans_Clusters"].apply(lambda x: x[i] if i < len(x) else np.nan)

# Fill NaN values with a default "No Cluster" placeholder (-1)
for i in range(max_columns):
    df[f"Cluster_{i+1}"].fillna(-1, inplace=True)

# Drop the original KMeans_Clusters column (optional)
df.drop(columns=["KMeans_Clusters"], inplace=True)

def get_next_cluster_and_update(row):
    # Extract the list of clusters for a person
    clusters = row[[f"Cluster_{i+1}" for i in range(10)]].tolist()
    
    # Find the last valid cluster before the first -1
    for i in range(len(clusters) - 1, -1, -1):  # Reverse loop
        if clusters[i] != -1:
            # Set this cluster as the next cluster
            next_cluster = clusters[i]
            # Replace this cluster with -1 in the sequence
            clusters[i] = -1
            # Update the row with modified cluster sequence
            for j in range(len(clusters)):
                row[f"Cluster_{j+1}"] = clusters[j]
            return next_cluster  # Return the next cluster
    
    return np.nan  # If no valid cluster exists

# Apply the function to create the target variable and update clusters
df["Next_Cluster"] = df.apply(get_next_cluster_and_update, axis=1)

# Drop rows with no valid target (optional)
df = df.dropna(subset=["Next_Cluster"])

# Ensure Next_Cluster is an integer
df["Next_Cluster"] = df["Next_Cluster"].astype(int)

# Select a specific person (e.g., row index 1000)
df["Geo Location"] = df_init["Geo Location"]
first_person = df.iloc[11]

# Load original confirmed locations from 'Geo Location'
geo_data = json.loads(first_person["Geo Location"])

# Extract confirmed locations, ensuring 'location' key exists
confirmed_locations = [
    {"city": marker["label"], "lat": marker["location"]["lat"], "lon": marker["location"]["lon"]}
    for marker in geo_data.get("markers", []) if "location" in marker
]

# Extract the predicted next cluster
next_cluster = first_person["Next_Cluster"]

# Calculate city frequencies to weight less common locations
city_frequency = {city: 1 for city in city_location_mapping.keys()}  # Default freq = 1
for city in city_location_mapping.keys():
    city_frequency[city] += 1  # Count occurrences (higher → penalized)

# Function to get multiple nearby valid cities with weighted probability
def get_balanced_prediction(cluster_id, last_known_location, min_distance_km=100, max_distance_km=1500, num_choices=7):
    """
    Finds multiple nearby cities with a weighted probability but ensures
    the predicted step is neither too close nor too far.
    """
    city_options = []

    for city, data in city_location_mapping.items():
        city_coords = (data["lat"], data["lon"])
        try:
            distance = geodesic(last_known_location, city_coords).kilometers
            if min_distance_km <= distance <= max_distance_km:
                # Compute weight: Favor less frequent locations & avoid tiny jumps
                weight = 1 / (city_frequency.get(city, 1) + 1)
                adjusted_weight = weight * ((distance - min_distance_km) / (max_distance_km - min_distance_km + 1))  
                city_options.append((city, data["lat"], data["lon"], distance, adjusted_weight))
        except:
            continue  # Ignore invalid values

    # Sort by distance & select the top `num_choices` closest ones
    city_options = sorted(city_options, key=lambda x: x[3])[:num_choices]

    if not city_options:
        return None  # No valid options

    # Normalize weights for probability selection
    total_weight = sum(city[4] for city in city_options)
    probabilities = [city[4] / total_weight for city in city_options]

    # Select a city using weighted probabilities
    selected_city = random.choices(city_options, weights=probabilities, k=1)[0]
    
    return {"city": selected_city[0], "lat": selected_city[1], "lon": selected_city[2]}

# Ensure we have at least one valid confirmed location
if confirmed_locations:
    map_center = (confirmed_locations[0]["lat"], confirmed_locations[0]["lon"])
    last_location = (confirmed_locations[-1]["lat"], confirmed_locations[-1]["lon"])
else:
    print("⚠️ No confirmed locations found for this person.")
    map_center = (0, 0)
    last_location = (0, 0)  # Default to prevent errors

# Get a more realistic prediction with balanced selection
realistic_prediction = get_balanced_prediction(next_cluster, last_location)

# Create **Folium Map with a Vintage Tile Layer**
m = folium.Map(
    location=map_center,
    zoom_start=6,
    tiles="Stamen Toner",  # WWII-style black and white map
    attr="Stamen Toner (Historical Map)"
)

# 🔹 **Improved Sepia Overlay for Vintage War Look**
sepia_overlay = "https://cdn.pixabay.com/photo/2016/11/13/21/49/background-1822153_1280.jpg"  # High-resolution sepia texture

# folium.raster_layers.ImageOverlay(
#     name="Sepia Tint Overlay",
#     image=sepia_overlay,
#     bounds=[[-85, -180], [85, 180]],  # Expanded for full global coverage
#     opacity=0.4,  # Slightly stronger sepia effect
#     interactive=False
# ).add_to(m)

# 🔹 **Alternative: Tile-Based Overlay for Better Scaling**
folium.TileLayer(
    tiles="https://www.transparenttextures.com/patterns/old-map.png",  # Old map texture
    attr="Old Map Texture",
    name="Sepia War Map",
    overlay=True,
    control=True
).add_to(m)


# 🔹 **Confirmed Locations - Default Dark Red Markers**
for i, point in enumerate(confirmed_locations):
    folium.Marker(
        location=[point["lat"], point["lon"]],
        popup=f"Confirmed Step {i+1}: {point['city']}",
        icon=folium.Icon(color="darkred", icon="info-sign")  # Default marker in dark red
    ).add_to(m)

# 🔹 **Draw Paths with Aged Sepia Colors**
for i in range(len(confirmed_locations) - 1):
    folium.PolyLine(
        [(confirmed_locations[i]["lat"], confirmed_locations[i]["lon"]),
         (confirmed_locations[i+1]["lat"], confirmed_locations[i+1]["lon"])],
        color="#704214",  # Sepia war-map style
        weight=3
    ).add_to(m)

# 🔹 **Predicted Next Step - Flag Icon**
if realistic_prediction:
    folium.Marker(
        location=[realistic_prediction["lat"], realistic_prediction["lon"]],
        popup=f"Predicted Next Step: {realistic_prediction['city']}",
        icon=folium.Icon(color="orange", icon="flag")  # Default flag icon in orange
    ).add_to(m)

    # Draw a dashed **orange line** from the last confirmed stop to the corrected predicted stop
    folium.PolyLine(
        [(confirmed_locations[-1]["lat"], confirmed_locations[-1]["lon"]),
         (realistic_prediction["lat"], realistic_prediction["lon"])],
        color="orange",
        weight=2.5,
        dash_array="5,5"
    ).add_to(m)

# 🔹 **Layer Control: Toggle WWII vs Modern Map**
folium.TileLayer("CartoDB Positron", name="Modern Map").add_to(m)  # Light gray for modern
folium.LayerControl(collapsed=False).add_to(m)  # Control for toggling maps



# ✅ **Final Output: Vintage War Map**
m.save("vintage_war_map.html")
m
