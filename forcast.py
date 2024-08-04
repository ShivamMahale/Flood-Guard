import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import folium
from streamlit_folium import st_folium

geolocator = Nominatim(user_agent="weather_app")

# Function to fetch coordinates for a given location
def get_coordinates(location_name):
    try:
        location = geolocator.geocode(location_name)
        if location:
            return location.latitude, location.longitude
        else:
            st.error("Location not found.")
            return None, None
    except GeocoderTimedOut:
        st.error("Geocoding service timed out.")
        return None, None

# Function to fetch weather data from Open-Meteo API

def fetch_weather_data(latitude, longitude):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": [
            "temperature_2m", "relative_humidity_2m", "precipitation", "rain", 
            "pressure_msl", "surface_pressure", "evapotranspiration", 
            "vapour_pressure_deficit", "wind_speed_10m", "wind_direction_120m", 
            "soil_temperature_18cm", "soil_moisture_1_to_3cm"
        ]
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def forcast_page():

    # CSS for styling
    st.markdown("""
        <style>
        .main-title {
            font-size: 2.5rem;
            font-weight: 600;
            text-align: center;
            margin-bottom: 2rem;
        }
        .sub-title {
            font-size: 1.5rem;
            font-weight: 500;
            text-align: center;
            margin-bottom: 1.5rem;
        }
        .location-input {
            display: flex;
            justify-content: center;
            margin-bottom: 2rem;
        }
        .fetching-data {
            font-size: 1rem;
            text-align: center;
            color: gray;
            margin-bottom: 2rem;
        }
        .data-title {
            font-size: 1.5rem;
            font-weight: 500;
            text-align: center;
            margin-top: 2rem;
            margin-bottom: 1rem;
        }
        .chart-container {
            justify-content: space-between;
            margin-top: 2rem;
            margin-bottom: 2rem;
        }
        .chart {
            width: 32%;
            margin-right: 1%;
        }
        .chart:last-child {
            margin-right: 0;
        }
        .background-image {
            background-image: url('https://images.pexels.com/photos/40784/drops-of-water-water-nature-liquid-40784.jpeg');
            background-size: cover;
            background-position: center;
            padding: 8rem;
            margin-top: 1rem;
            margin-bottom: 1rem;
        }
        .centered-title {
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)
    st.markdown('<h1 class="centered-title">Weather Lens</h1>', unsafe_allow_html=True)
    st.markdown('<div class="background-image">', unsafe_allow_html=True)
    st.markdown('<div class="main-title">User can uncover global weather trends with a tap.</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Select a location to visualize its hourly forecasted weather data.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Location input
    st.markdown('<div class="location-input">', unsafe_allow_html=True)
    location_name = st.text_input("Enter location (e.g., London, New York)")
    st.markdown('</div>', unsafe_allow_html=True)
    fetch_button = st.button("Fetch Weather Data")

    if fetch_button and location_name:
        latitude, longitude = get_coordinates(location_name)
        
        if latitude and longitude:
        
            # Fetch the data
            weather_data = fetch_weather_data(latitude, longitude)
            # Process the data
            hourly = weather_data['hourly']
            hourly_time = hourly['time']
            
            # Extract units
            units = weather_data['hourly_units']

            # Create DataFrame
            hourly_data = {"date": pd.to_datetime(hourly_time, utc=True)}
            for key in units.keys():
                hourly_data[key] = hourly[key]

            hourly_dataframe = pd.DataFrame(data=hourly_data)
            # Convert to daily data by taking mean of each day
            hourly_dataframe['day'] = hourly_dataframe['date'].dt.date
            daily_dataframe = hourly_dataframe.groupby('day').mean(numeric_only=True).reset_index()


            # Visualization
            st.markdown(f'<div class="data-title">Hourly Forecast Weather Data for {location_name}</div>', unsafe_allow_html=True)

            # Define parameters to plot
            params_to_plot = [
                ("temperature_2m", "Temperature", "red"),
                ("relative_humidity_2m", "Relative Humidity", "blue"),
                ("precipitation", "Precipitation", "green"),
                ("rain", "Rain", "purple"),
                ("pressure_msl", "Pressure (MSL)", "orange"),
                ("surface_pressure", "Surface Pressure", "brown"),
                ("evapotranspiration", "Evapotranspiration", "pink"),
                ("vapour_pressure_deficit", "Vapour Pressure Deficit", "cyan"),
                ("wind_speed_10m", "Wind Speed (10m)", "yellow"),
                ("wind_direction_120m", "Wind Direction (120m)", "violet"),
                ("soil_temperature_18cm", "Soil Temperature (18cm)", "lime"),
                ("soil_moisture_1_to_3cm", "Soil Moisture (1-3cm)", "magenta")
            ]

            # Create charts in a 3-column layout
            cols = st.columns(3)
            for i, (param, title, color) in enumerate(params_to_plot):
                if param in hourly_dataframe.columns:
                    fig = px.line(hourly_dataframe, x='date', y=param, 
                                title=f'Hourly {title} in {units[param]}',
                                labels={param: f'{title} ({units[param]})'})
                    fig.update_layout(title_font_size=18, title_font_color='darkblue', title_x=0.5, title_xanchor='center')
                    fig.update_traces(line_color=color, line_width=2)
                    fig.update_layout(height=400)  # Set fixed height
                    cols[i % 3].plotly_chart(fig, use_container_width=True)


            # Define parameters to plot for pie charts
            params_to_plot_pie = [
                ("temperature_2m", "Temperature"),
                ("relative_humidity_2m", "Relative Humidity"),
                ("precipitation", "Precipitation"),
                ("rain", "Rain"),
                ("pressure_msl", "Pressure (MSL)"),
                ("surface_pressure", "Surface Pressure"),
                ("evapotranspiration", "Evapotranspiration"),
                ("vapour_pressure_deficit", "Vapour Pressure Deficit"),
                ("wind_speed_10m", "Wind Speed (10m)"),
                ("wind_direction_120m", "Wind Direction (120m)"),
                ("soil_temperature_18cm", "Soil Temperature (18cm)"),
                ("soil_moisture_1_to_3cm", "Soil Moisture (1-3cm)")
            ]

            # Iterate through parameters and create pie charts
            cols = st.columns(2)  # Create two columns for pie charts
            for i, (param, title) in enumerate(params_to_plot_pie):
                if param in daily_dataframe.columns:
                    unit = units.get(param, '')  # Get the unit for the current parameter
                    fig_pie = px.pie(daily_dataframe, names='day', values=param, 
                                    title=f'Average Daily {title} Distribution ({unit})')
                    fig_pie.update_layout(margin=dict(t=50, b=0, l=0, r=0), height=450, title_x=0.5, title_xanchor='center')
                    cols[i % 2].plotly_chart(fig_pie, use_container_width=True)

            # Table of data
            st.write('Hourly Weather Data')
            st.dataframe(hourly_dataframe)

            st.write('Daily Weather Data')
            st.dataframe(daily_dataframe)
                    
    # Custom CSS to add some padding and style
    st.markdown("""
        <style>
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .stPlotlyChart {
            padding-top: 2rem;
            padding-bottom: 1rem;
        }
        </style>
        """, unsafe_allow_html=True)
