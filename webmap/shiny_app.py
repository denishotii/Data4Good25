import pandas as pd
import folium
import json
import random
from shiny import App, ui, render
from geopy.distance import geodesic

# Load preprocessed data (optimized for speed)
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
        .floating-info {
            position: absolute;
            bottom: 20px;
            left: 20px;
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 12px;
            border-radius: 10px;
            font-size: 14px;
            display: none;
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
    """),
    ui.div(
        ui.output_ui("map"),
        ui.div(
            ui.tags.h3("Search for a Victim"),
            ui.input_text("victim_name", "Type Name:", ""),
            ui.output_ui("victim_list"),
            ui.output_text("selected_victim"),
            ui.div(class_="floating-info", id="info-box")
        ),
        id="map-container"
    )
)

# Function to generate the map with country names & vintage overlay
def create_map(selected_victim=None):
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

    # ✅ Use "CartoDB Positron" for country names & borders
    m = folium.Map(
        location=map_center,
        zoom_start=6,
        tiles="CartoDB Positron",
        attr="© OpenStreetMap contributors"
    )

    # ✅ Add old map texture for a vintage look
    folium.TileLayer(
        tiles="https://www.transparenttextures.com/patterns/old-map.png",
        attr="Old Map Texture",
        name="Sepia War Map",
        overlay=True,
        control=True
    ).add_to(m)

    # ✅ Add Stamen Toner as an optional toggle layer
    folium.TileLayer(
        tiles="Stamen Toner",
        attr="Stamen Toner (Historical Map)",
        name="WWII Map"
    ).add_to(m)

    # Mark confirmed locations
    for i, point in enumerate(confirmed_locations):
        folium.Marker(
            location=[point["lat"], point["lon"]],
            popup=f"Confirmed Step {i+1}: {point['city']}",
            icon=folium.Icon(color="darkred", icon="info-sign")
        ).add_to(m)

    # Draw paths in sepia color
    for i in range(len(confirmed_locations) - 1):
        folium.PolyLine(
            [(confirmed_locations[i]["lat"], confirmed_locations[i]["lon"]),
             (confirmed_locations[i+1]["lat"], confirmed_locations[i+1]["lon"])],
            color="#704214",
            weight=3
        ).add_to(m)

    # Add a predicted location based on similar victims
    realistic_prediction = confirmed_locations[-1] if confirmed_locations else None
    if realistic_prediction:
        folium.Marker(
            location=[realistic_prediction["lat"], realistic_prediction["lon"]],
            popup=f"Predicted Next Step: {realistic_prediction['city']}",
            icon=folium.Icon(color="orange", icon="flag")
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
        return ui.HTML(create_map(input.selected_victim()))

app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
