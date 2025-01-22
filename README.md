# Team Unconstrained | Data4Good Berlin 

## Table of Contents
- [Introduction](#introduction)
- [Importance of the Arolsen Archives & Project Impact](#importance-of-the-arolsen-archives--project-impact)
- [Project Structure](#project-structure)
- [Project Organization](#project-organization)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
    - [Jupyter Notebooks](#jupyter-notebooks)
    - [Web Application](#web-application)
    - [Predicting Victims Geo Locations](#predicting-victims-geo-locations)
- [Analysis Steps](#analysis-steps)
    - [Initial Setup](#initial-setup)
    - [Exploratory Data Analysis and Visualization](#exploratory-data-analysis-and-visualization)
    - [Route and Station Popularity](#route-and-station-popularity)
    - [Demand Analysis](#demand-analysis)
    - [Unused Stops](#unused-stops)
- [Conclusion](#conclusion)
- [Collaborators](#collaborators)

## Introduction
This project identifies patterns in imprisonment locations during the Holocaust. The analysis is performed using Python and Jupyter Notebooks.

Visit our platform in the following [link](https://linktr.ee/data4good_unconstrained).

## Importance of the Arolsen Archives & Project Impact  

The **Arolsen Archives** hold the world’s most comprehensive collection of documents related to **Nazi persecution**, serving as a critical resource for Holocaust research. These archives contain millions of records that help families trace lost relatives and provide historians with vital evidence of past atrocities.  

Our project **enhances the accessibility and interpretability** of these records by transforming raw data into an **interactive visual tool**. By doing so, we:  

- **Support researchers** in identifying overlooked patterns in persecution.  
- **Assist families** in better understanding the journeys of their lost relatives.  
- **Contribute to Holocaust education**, ensuring that history is preserved and remains relevant to future generations.  

This project stands as a testament to the **power of data science in historical research**, bridging the gap between **fragmented historical records and modern analytical tools**.  

## Project Structure

- `data/`: Directory containing the input data files (Not Publicly Available).
- `webmap/`: Directory containing the web application for visualizing the data on an interactive map.
- `prepare_data_for_powerbi.ipynb`: Jupyter Notebook for preparing data for Power BI visualization.
- `geolocation_patterns.ipynb`: Jupyter Notebook for analyzing geolocation patterns.
- `geolocation_map_prediction.ipynb`: Jupyter Notebook for predicting geolocation on the map.
- `Data Cleaning+OneHotEncoding, Markov Chain.ipynb`: Jupyter Notebook for data cleaning, one-hot encoding, and Markov Chain analysis.

## Project Organization

    ├── data                    <- Directory containing the input data files
    ├── frontend                <- Vite+React Application for our Frontend
    ├── webmap                  <- Directory containing the web application for visualizing the data on an interactive map.
    ├── Data Cleaning+OneHotEncoding, Markov Chain.ipynb    <- initial data exploration and profiling
    ├── geolocation_patterns.ipynb                          <- Notebook containing the data analysis and visualization for geolocations
    ├── README.md                                           <- The top-level README for developers using this project.
    ├── requirements.txt                                    <- Python requirements
    ├── LICENSE                                             <- MIT License
    └── Accenture_Arolsen_Handout.pdf                       <- Challenge PDF

---

## Technologies Used
- **Python** 
- **Pandas**         (Dataframe)
- **Scikit-learn** 
   - **Surprise**    (for collaborative filtering)
- **Matplotlib**     (for data visualization)
- **Seaborn**        (for data visualization)
- **Squarify**       (for data visualization-Tree Map)
- **ydata_profiling**       (for data analysis)
- **Axios**: A promise-based HTTP client for the browser and Node.js.
- **Bootstrap**: A popular CSS framework for developing responsive and mobile-first websites.
- **Font Awesome**: A toolkit for vector icons and social logos.
- **ShinyApp**: A web framework for developing web applications, originally in R and since 2022 in python.
- **Google Maps API**: Used for showing the map on the web data visualization
- **Folium**: Used to show marks and heatmap on the Map
- **Microsoft Power BI**:  Is an interactive data visualization software product, used to create interactive data charts
- **Dora Web Builder**: Used to create the presentation website

## Setup Instructions

1. **Clone the repository:**
    ```sh
    git clone https://github.com/denishotii/Data4Good25.git
    cd Data4Good25
    ```

2. **Create a virtual environment:**
    ```sh
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Install additional packages used in the notebooks:**
    ```sh
    pip install numpy matplotlib pandas folium ydata_profiling scikit-learn googlemaps shiny
    ```

## Usage

### Jupyter Notebooks

1. **Run the Jupyter Notebook server:**
    ```sh
    jupyter notebook
    ```

2. **Open `main.ipynb` and `AnalyseDataset.ipynb` in the Jupyter Notebook interface.**

3. **Follow the steps in the notebooks to perform the data analysis and visualization.**

### Web Application

1. **Navigate to the `webmap` directory:**
    ```sh
    cd webmap
    ```

2. **Run the web application:**
    ```sh
    python app.py
    ```

3. **Open your web browser and go to `http://127.0.0.1:8000` to view the interactive map.**

### Predicting Victims Geo Locations

1. **Run the prediction model:**
    ```sh
    Open and run the notebook: geolocation_map_prediction.ipynb
    ```

2. **The model will predict possible routes of persecution by identifying patterns from similar records.**

## Analysis Steps

To achieve the goal of mapping and analyzing the movement of Holocaust victims based on tracing card data, we implemented the following steps:

### 1. Data Preprocessing and Cleaning  
- Standardized name variations and handled missing values.  
- Extracted and structured relevant columns, including **birthplace, nationality, geolocation, and validation score**.  
- Implemented similarity measures to merge duplicate records and ensure data consistency.  

### 2. Geographic Visualization of Victim Routes  
- Utilized the **Geo Location** field to map known locations of individuals.  
- Developed an interactive map that visualizes movement patterns and key transit points.  
- Enabled search functionality to filter individuals by name, date, and location.  

### 3. Pattern Analysis and Route Prediction  
- Applied clustering techniques and similarity measures to group victims with similar routes.  
- Used machine learning models to **predict possible missing transit locations** based on known paths.  
- Designed an algorithm to infer unlisted stops based on historically documented patterns of deportation.  

### 4. Validation and Confidence Scoring  
- Integrated **OCR validation** to assess the trustworthiness of extracted data.  
- Applied manual and automated review processes to enhance data accuracy.  
- Ensured **automated verification flags** help prioritize records needing manual validation. 

## Conclusion  

This project successfully provides a **historical geographic analysis tool** that reconstructs the journeys of Holocaust victims. By combining **data visualization, predictive modeling, and validation techniques**, we help uncover **patterns in forced migration**, filling gaps in historical records.  

### Key takeaways:  
**Mapped and analyzed** known victim transport routes using structured data.  
**Inferred missing transit points**, improving the completeness of historical records.  
**Supported educational and research efforts** by offering an interactive and data-driven understanding of victim movements.  

This initiative serves as a **step forward in digital humanities**, demonstrating how data science can be used for historical preservation and awareness.  

## Collaborators

- [Denis Hoti](https://www.linkedin.com/in/denishoti/)
- [Veronika Rybak](https://www.linkedin.com/in/veronika-rybak-55379a337/)
- [Ali Guliyev](https://www.linkedin.com/in/ali-guliyev-389837238/)
- [Ruslan Tsibirov](https://www.linkedin.com/in/ruslan-tsibirov-6bb6a2262/)
- [Olga Ivanova](https://github.com/olyashevich)