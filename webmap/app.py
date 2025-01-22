import pandas as pd
import folium
import json
import random
from shiny import App, ui, render
from geopy.distance import geodesic

# Load preprocessed data
df = pd.read_csv("data/cleaned_holocaust_data.csv")

# Ensure missing names are replaced with "Unknown"
victim_dict = {}
for _, row in df.iterrows():
    if not pd.isna(row["Geo Location"]):
        last_name = str(row["Last_Name"]) if not pd.isna(row["Last_Name"]) else "Unknown"
        first_name = str(row["First Name"]) if not pd.isna(row["First Name"]) else "Unknown"
        full_name = f"{last_name}, {first_name}"

        try:
            victim_dict[full_name] = json.loads(row["Geo Location"])
        except json.JSONDecodeError:
            continue

# Define UI layout
app_ui = ui.page_fluid(
    ui.tags.style("""
        body, html { margin: 0; padding: 0; height: 100%; overflow: hidden; }
        #map-container { height: 100vh; width: 100vw; position: relative; }
        #search-panel {
            position: absolute;
            top: 20px;
            left: 20px;
            background: rgba(255, 255, 255, 0.95);
            padding: 15px;
            border-radius: 12px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
            width: 300px;
            z-index: 1000;
        }              

        .victim-card {
            background: white;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 5px;
            cursor: pointer;
            border: 1px solid #ddd;
        }
        .victim-card:hover {
            background: #f0f0f0;
        }
                  
        .shiny-spinner-container {
            opacity: 0 !important; /* Make it invisible */
            pointer-events: none; /* Prevent interaction */
        }
    """),
    ui.div(
        ui.div(
            ui.tags.h3("Search for a Victim"),
            ui.input_text("victim_name", "Type Name:", "", autocomplete="off"),
            ui.output_ui("victim_list"),
            ui.output_text("selected_victim"),
            ui.input_checkbox("show_prediction", "Show Predicted Next Step", value=True),
            id="search-panel"
        ),
        ui.output_ui("map"),
        id="map-container"
    )


)

ui.tags.script("""
    var debounceTimer;
    document.addEventListener("DOMContentLoaded", function() {
        var input = document.querySelector('input[id="victim_name"]');
        if (input) {
            input.addEventListener("input", function() {
                clearTimeout(debounceTimer);
                debounceTimer = setTimeout(function() {
                    Shiny.setInputValue('victim_name', input.value, {priority: 'event'});
                }, 500); // 500ms debounce delay
            });
        }
    });
""")


import math

def generate_example_next_step(last_location):
    """
    Generates a fake next step by moving the location in a random direction 
    between 300 km and 1500 km away.
    """
    if not last_location:
        return None

    lat, lon = last_location

    # Generate a random direction (angle in degrees)
    random_angle = random.uniform(0, 360)

    # Generate a random distance (between 300 km and 1500 km)
    random_distance = random.uniform(300, 700)  # in km

    # Earth's radius in km
    earth_radius = 6371.0

    # Convert distance to radians
    angular_distance = random_distance / earth_radius

    # Convert angle to radians
    random_angle_rad = math.radians(random_angle)

    # Calculate new latitude
    new_lat = math.asin(math.sin(math.radians(lat)) * math.cos(angular_distance) +
                         math.cos(math.radians(lat)) * math.sin(angular_distance) * math.cos(random_angle_rad))

    # Calculate new longitude
    new_lon = math.radians(lon) + math.atan2(math.sin(random_angle_rad) * math.sin(angular_distance) * math.cos(math.radians(lat)),
                                             math.cos(angular_distance) - math.sin(math.radians(lat)) * math.sin(new_lat))

    # Convert back to degrees
    new_lat = math.degrees(new_lat)
    new_lon = math.degrees(new_lon)

    return {"city": "Unknown (Example Prediction)", "lat": new_lat, "lon": new_lon}

# Modify the map function
def create_map(selected_victim=None, show_prediction=True):
    if not selected_victim or selected_victim not in victim_dict:
        return folium.Map()._repr_html_()

    data = victim_dict[selected_victim]
    confirmed_locations = [
        {"city": marker["label"], "lat": marker["location"]["lat"], "lon": marker["location"]["lon"]}
        for marker in data.get("markers", []) if "location" in marker
    ]

    if confirmed_locations:
        map_center = (confirmed_locations[0]["lat"], confirmed_locations[0]["lon"])
        last_location = (confirmed_locations[-1]["lat"], confirmed_locations[-1]["lon"])
    else:
        map_center = (0, 0)
        last_location = (0, 0)

    m = folium.Map(
        location=map_center,
        zoom_start=6,
        tiles="CartoDB Positron",
        attr="© OpenStreetMap contributors"
    )

    folium.TileLayer(
        tiles="https://www.transparenttextures.com/patterns/old-map.png",
        attr="Old Map Texture",
        name="Sepia War Map",
        overlay=True,
        control=True
    ).add_to(m)

    folium.TileLayer(
        tiles="Stamen Toner",
        attr="Stamen Toner (Historical Map)",
        name="WWII Map"
    ).add_to(m)

    for i, point in enumerate(confirmed_locations):
        folium.Marker(
            location=[point["lat"], point["lon"]],
            popup=f"Confirmed Step {i+1}: {point['city']}",
            icon=folium.Icon(color="darkred", icon="info-sign")
        ).add_to(m)

    for i in range(len(confirmed_locations) - 1):
        folium.PolyLine(
            [(confirmed_locations[i]["lat"], confirmed_locations[i]["lon"]),
             (confirmed_locations[i+1]["lat"], confirmed_locations[i+1]["lon"])],
            color="#704214",
            weight=3
        ).add_to(m)

    if show_prediction:
        fake_prediction = generate_example_next_step(last_location)
        if fake_prediction:
            folium.Marker(
                location=[fake_prediction["lat"], fake_prediction["lon"]],
                popup=f"Predicted Next Step: {fake_prediction['city']}",
                icon=folium.Icon(color="orange", icon="flag")
            ).add_to(m)

            folium.PolyLine(
                [(confirmed_locations[-1]["lat"], confirmed_locations[-1]["lon"]),
                 (fake_prediction["lat"], fake_prediction["lon"])],
                color="orange",
                weight=2.5,
                dash_array="5,5"
            ).add_to(m)

    folium.LayerControl(collapsed=False).add_to(m)
    return m._repr_html_()


# Define server-side logic
def server(input, output, session):
    @output
    @render.ui
    def victim_list():
        query = input.victim_name().strip().lower()
        if not query:
            return ui.HTML("")

        matches = [name for name in victim_dict.keys() if query in name.lower()]
        if not matches:
            return ui.HTML("<p>No results found</p>")

        return ui.HTML("".join([
            f'<div class="victim-card" '
            f'onclick="Shiny.setInputValue(\'selected_victim\', \'{name}\', {{priority: \'event\'}});">'
            f'{name}</div>'
            for name in matches[:5]
        ]))

    @output
    @render.ui
    def map():
        return ui.HTML(create_map(input.selected_victim(), input.show_prediction()))

app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
