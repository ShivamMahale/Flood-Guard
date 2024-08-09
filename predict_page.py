import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
import db
import notification
from streamlit.components.v1 import html
import forcast as fc

# Ensure the keys exist in session state
if 'location_name' not in st.session_state:
    st.session_state['location_name'] = None
if 'weather_data' not in st.session_state:
    st.session_state['weather_data'] = None
if 'iot_data_fetched' not in st.session_state:
    st.session_state['iot_data_fetched'] = False

# Function to fetch coordinates and weather data
def fetch_coordinates_and_weather(location_name):
    latitude, longitude = fc.get_coordinates(location_name)
    if latitude and longitude:
        weather_data = fc.fetch_weather_data(latitude, longitude)
        return weather_data
    return None

# Placeholder function for the model prediction

def predict_model(input_data):
    # Load the model from the file
    #filename = 'LR_model.pkl'
    filename = os.path.join('model', 'LR_model.pkl')
    loaded_model = pickle.load(open(filename, 'rb'))
    # Ensure input_data is in the correct shape (for a single prediction)
    input_array = np.array(input_data).reshape(1, -1)
    # Make the prediction
    prediction = loaded_model.predict(input_array)
    
    return prediction[0]  # Assuming prediction is an array
    

def predict_page():
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
            background-image: url('https://images.pexels.com/photos/6802042/pexels-photo-6802042.jpeg?auto=compress&cs=tinysrgb&w=600');
            background-size: cover;
            background-position: center;
            padding: 11rem;
            margin-top: 1rem;
            margin-bottom: 1rem;
        }
        .centered-title {
            text-align: center;
        }
        .stNumberInput input {
        max-width: 100px;
        margin: 0 auto;
        text-align: center;
    }
    .custom-form {
        background-color: #f1f1f1;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
    }
    .custom-form .stButton button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 24px;
        border-radius: 5px;
        cursor: pointer;
    }
    .custom-form .stButton button:hover {
        background-color: #45a049;
    }
        </style>
    """, unsafe_allow_html=True)
    st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">', unsafe_allow_html=True)
    st.markdown('<h1 class="centered-title">Flood Probability Predictor <i class="fas fa-rocket"></i></h1>', unsafe_allow_html=True)
    st.markdown('<div class="background-image">', unsafe_allow_html=True)
    st.markdown('<div class="main-title">Enhance Preparedness with Precise Flood Risk Estimates</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Enter the location name to predict probability of flood by fetchning latest IOT Data</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    # Location input
    st.markdown('<div class="location-input">', unsafe_allow_html=True)
    location_name = st.text_input("Enter location (e.g., London, New York)",value=st.session_state['location_name'])
    st.markdown('</div>', unsafe_allow_html=True)
    fetch_button = st.button("Fetch IOT Data",key="fetch")
    if fetch_button and location_name:
         weather_data = fetch_coordinates_and_weather(location_name)
         if weather_data:
            st.session_state['weather_data'] = weather_data
            st.session_state['location_name'] = location_name
            st.session_state['iot_data_fetched'] = True
   
    # Only call predict_iot_data if the IOT data has been fetched
    if st.session_state['iot_data_fetched']:
        predict_iot_data(st.session_state['weather_data'],st.session_state['location_name'])
    with st.expander("User Data Prediction", expanded=False):
        predict_user_data()

def predict_user_data():
    fields = ["MonsoonIntensity", "TopographyDrainage", "RiverManagement", "Deforestation", "Urbanization", "ClimateChange", "DamsQuality", "Siltation", "AgriculturalPractices", "Encroachments", "IneffectiveDisasterPreparedness", "DrainageSystems", "CoastalVulnerability", "Landslides", "Watersheds", "DeterioratingInfrastructure", "PopulationScore", "WetlandLoss", "InadequatePlanning", "PoliticalFactors"]

    st.subheader("Provide the input values in range 0 to 20")

    with st.form(key='user_data_form'):
        input_values = []
        for field in fields:
            value = st.number_input(f"{field}", min_value=0, max_value=20, value=5)
            input_values.append(value)
        submit_button = st.form_submit_button(label='Predict User Data')

    if submit_button:
        input_df = pd.DataFrame([input_values], columns=fields)
        prediction = predict_model(input_values)
        prediction_percent = prediction * 100
        
        if prediction > 0.50:
            send_email(prediction_percent)
        
        display_prediction_card(prediction_percent, "User")

def predict_iot_data(weather_data,location_name):
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

        # Get the current day's data
        current_day_data = daily_dataframe.iloc[0]
    

        st.markdown(f'<div class="data-title">Todays Average Weather Data for {location_name}</div>', unsafe_allow_html=True)
        # Define parameters to display with corresponding icons and colors
        params_to_display = [
            ("temperature_2m", "Temperature", "fas fa-thermometer-half", "rgba(255, 99, 71, 0.5)"),
            ("relative_humidity_2m", "Relative Humidity", "fas fa-tint", "rgba(135, 206, 235, 0.5)"),
            ("precipitation", "Precipitation", "fas fa-cloud-rain", "rgba(173, 216, 230, 0.5)"),
            ("rain", "Rain", "fas fa-cloud-showers-heavy", "rgba(0, 191, 255, 0.5)"),
            ("wind_speed_10m", "Wind Speed (10m)", "fas fa-wind", "rgba(176, 224, 230, 0.5)"),
            ("pressure_msl", "Pressure (MSL)", "fas fa-tachometer-alt", "rgba(255, 228, 181, 0.5)")
        ]
        # Create a 3-column layout
        cols = st.columns(3)
        for i, (param, title, icon_class, bg_color) in enumerate(params_to_display):
            if param in current_day_data.index:
                unit = units.get(param, '')  # Get the unit for the current parameter
                card_html = f"""
                <div style="
                    background-color: {bg_color};
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    margin-top: 20px;
                    text-align: center;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                ">
                    <i class="{icon_class}" style="font-size: 50px;"></i>
                    <h4>{title}</h4>
                    <p><strong>{current_day_data[param]} {unit}</strong></p>
                </div>
                """
                cols[i % 3].markdown(card_html, unsafe_allow_html=True)

        # SQL query to fetch the first 10 records
        query = "SELECT * FROM iot_data ORDER BY RAND() LIMIT 1"
        iot_op_df = db.fetch_iot_output_data(query)
        # Exclude a specific column from the DataFrame
        columns_to_exclude = ['created_at', 'id','FloodProbability']
        latest_iot_data = iot_op_df.drop(columns=columns_to_exclude)
        if latest_iot_data is not None:
            st.markdown(f'<div class="data-title">Latest IOT Data for {location_name}</div>', unsafe_allow_html=True)
            st.dataframe(latest_iot_data)
            st.markdown('<div class="sub-title">Click on the prediction button to predict probability of flood for the above latest IOT Data</div>', unsafe_allow_html=True)
            # Call the prediction function
            predict_iot_button = st.button("Predict IOT Data",key="predictiotdata")
            if predict_iot_button:
                prediction = predict_model(latest_iot_data)
                prediction_percent = prediction * 100
                if prediction>0.50:
                    # sent alert to user
                    send_email(prediction_percent)
                display_prediction_card(prediction_percent,"IOT")
        else:
            st.error("Failed to fetch Daily Report data from database")
            

def send_email(prediction_percent):
    to_address = st.session_state.email_id
    name = st.session_state.username
    subject = "Urgent: Flood Alert Notification"
    body = f"""
            <html>
            <body>
                <h4>Dear {name},</h4>
                <p>This is an automated alert to inform you of a potential flood risk in your area. Based on our latest analysis, there is a <strong>high probability</strong> of flooding.</p>
                <p><strong>Flood Probability: {prediction_percent:.2f}%</strong></p>
                <p>We strongly advise you to take the following precautions immediately:</p>
                <ul>
                    <li>Move valuable items and important documents to higher ground.</li>
                    <li>Prepare an emergency kit with essential items such as food, water, and medications.</li>
                    <li>Stay tuned to local news and weather reports for updates.</li>
                    <li>Follow any evacuation orders issued by local authorities.</li>
                </ul>
                <p>For more information and detailed guidance on flood preparedness, please visit our website or contact our support team.</p>
                <p>Stay safe,</p>
                <p>Flood Monitoring and Alert System</p>
            </body>
            </html>
            """
    notification.send_email(to_address, subject, body)
    st.success(f"Email sent successfully to {to_address}")


def display_prediction_card(prediction_percent,type):
    card_html = f"""
    <div style="
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin-top: 20px;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
        text-align: center;
        font-size: 20px;
        ">
        <h2>{type} Data Prediction Result</h2>
        <p>The predicted flood probability is: <strong>{prediction_percent:.2f}%</strong></p>
    </div>
    """
    html(card_html, height=200)

def display_current_weather_card(weather_data,location_name):
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

            # Get the current day's data
            current_day_data = daily_dataframe.iloc[0]
        

            st.markdown(f'<div class="data-title">Todays Average Weather Data for {location_name}</div>', unsafe_allow_html=True)
            # Define parameters to display with corresponding icons and colors
            params_to_display = [
                ("temperature_2m", "Temperature", "fas fa-thermometer-half", "rgba(255, 99, 71, 0.5)"),
                ("relative_humidity_2m", "Relative Humidity", "fas fa-tint", "rgba(135, 206, 235, 0.5)"),
                ("precipitation", "Precipitation", "fas fa-cloud-rain", "rgba(173, 216, 230, 0.5)"),
                ("rain", "Rain", "fas fa-cloud-showers-heavy", "rgba(0, 191, 255, 0.5)"),
                ("wind_speed_10m", "Wind Speed (10m)", "fas fa-wind", "rgba(176, 224, 230, 0.5)"),
                ("pressure_msl", "Pressure (MSL)", "fas fa-tachometer-alt", "rgba(255, 228, 181, 0.5)")
            ]
            # Create a 3-column layout
            cols = st.columns(3)
            for i, (param, title, icon_class, bg_color) in enumerate(params_to_display):
                if param in current_day_data.index:
                    unit = units.get(param, '')  # Get the unit for the current parameter
                    card_html = f"""
                    <div style="
                        background-color: {bg_color};
                        padding: 20px;
                        border-radius: 10px;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                        margin-top: 20px;
                        text-align: center;
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                    ">
                        <i class="{icon_class}" style="font-size: 50px;"></i>
                        <h4>{title}</h4>
                        <p><strong>{current_day_data[param]} {unit}</strong></p>
                    </div>
                    """
                    cols[i % 3].markdown(card_html, unsafe_allow_html=True)


    



    



