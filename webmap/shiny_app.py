import pandas as pd
import folium
import json
from shiny import App, ui, render

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
        ui.output_ui("map"),  # ✅ Must be placed first
        ui.div(
            ui.tags.h3("Search for a Victim"),
            ui.input_text("victim_name", "Type Name:", ""),
            ui.output_ui("victim_list"),
            ui.output_text("selected_victim"),
            ui.div(class_="floating-info", id="info-box")  # ✅ Order is now correct
        ),
        id="map-container"  # ✅ ID must come last
    )
)

# Function to generate map
def create_map(selected_victim=None):
    # ✅ Fixed the tiles issue
    m = folium.Map(
        location=[51.1657, 10.4515], 
        zoom_start=5,  
        tiles="OpenStreetMap",
        attr="© OpenStreetMap contributors"
    )

    if selected_victim and selected_victim in victim_dict:
        data = victim_dict[selected_victim]

        for i, marker in enumerate(data.get("markers", [])):
            folium.Marker(
                location=[marker["location"]["lat"], marker["location"]["lon"]],
                popup=f"{selected_victim} - {marker['label']}",
                icon=folium.Icon(color="red" if i == 0 else "blue")
            ).add_to(m)

        path_points = [(marker["location"]["lat"], marker["location"]["lon"]) for marker in data.get("markers", [])]
        folium.PolyLine(path_points, color="red", weight=3, dash_array="5,5").add_to(m)

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
