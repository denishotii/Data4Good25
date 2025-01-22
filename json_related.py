import json
import pandas as pd
import numpy as np
import pandas as pd
import seaborn as sns
from dataclasses import dataclass
from typing import List, Dict

data = pd.read_csv('Data4Good_Arolsen_Archives_50k.csv')


# Define the structure of Paths
@dataclass
class Path:
    From: str
    To: str
    Index: int
    Type: str

# Define the structure of Location inside Markers
@dataclass
class Location:
    Lat: float
    Lon: float

# Define the structure of Markers
@dataclass
class Marker:
    Location: Location
    Type: str
    Label: str

# Define the GeoLocation object that contains Paths and Markers
@dataclass
class GeoLocation:
    Paths: List[Path]
    Markers: List[Marker]

# Function to deserialize JSON into GeoLocation object
def deserialize_geo_location(json_text: str) -> GeoLocation:
    data = json.loads(json_text)

    # Deserialize Paths
    paths = [Path(**p) for p in data["Paths"]]

    # Deserialize Markers
    markers = [Marker(Location(**m["Location"]), m["Type"], m["Label"]) for m in data["Markers"]]

    return GeoLocation(Paths=paths, Markers=markers)

# Example JSON input (replace with actual JSON data)
json_text = '''
{
    "Paths": [
        {
            "From": "Berlin, Germany",
            "To": "Auschwitz, Poland",
            "Index": 1,
            "Type": "Camp Name"
        },
        {
            "From": "Auschwitz, Poland",
            "To": "Dachau, Germany",
            "Index": 2,
            "Type": "Camp Name"
        }
    ],
    "Markers": [
        {
            "Location": {
                "Lat": 52.5200,
                "Lon": 13.4050
            },
            "Type": "Birth Place",
            "Label": "Berlin, Germany"
        },
        {
            "Location": {
                "Lat": 50.0359,
                "Lon": 19.1783
            },
            "Type": "Camp Name",
            "Label": "Auschwitz, Poland"
        }
    ]
}
'''

# Deserialize JSON
geo_location_obj = deserialize_geo_location(data['Geo Location'][0])

# Print the resulting object
print(geo_location_obj)
print("\nFirst Path:", geo_location_obj.Paths[0])
print("\nFirst Marker:", geo_location_obj.Markers[0])