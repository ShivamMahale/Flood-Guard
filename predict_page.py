import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
import plotly.graph_objs as go
import plotly.express as px
import db
import notification
# Sample data

# Convert the data to a DataFrame
weather_df = pd.DataFrame(db.get_weather_data())

# Get the latest record
latest_record = weather_df.iloc[-1]

# Function to create a card for temperature
def create_temperature_card(temperature_info):
    st.subheader(f"Date: {temperature_info['date']}")
    st.write(f"Temperature: {temperature_info['temperature']} {temperature_info['temp_unit']}")
    st.write(f"Low: {temperature_info['temperature_low']} {temperature_info['temp_unit']}")
    st.write(f"High: {temperature_info['temperature_high']} {temperature_info['temp_unit']}")

    # Create a bar chart for temperature visualization with enhanced styling
    temp_df = pd.DataFrame({
        'Type': ['Current', 'Low', 'High'],
        'Temperature': [temperature_info['temperature'], temperature_info['temperature_low'], temperature_info['temperature_high']]
    })

    fig = px.bar(temp_df, x='Type', y='Temperature', title="Temperature", color='Type', 
                 color_discrete_map={'Current': 'royalblue', 'Low': 'lightblue', 'High': 'red'})
    
    fig.update_traces(marker_line_color='black', marker_line_width=1.5, opacity=0.6)
    fig.update_layout(width=400, height=300, title_font_size=16, title_x=0.5, title_y=0.95)
    fig.update_yaxes(title_text='Temperature (°C)')
    fig.update_xaxes(title_text='')
    
    st.plotly_chart(fig)

# Function to create a card for atmospheric pressure
def create_pressure_card(pressure_info):
    st.subheader(f"Date: {pressure_info['date']}")
    st.write(f"Pressure: {pressure_info['pressure']} {pressure_info['unit']}")
    st.write(f"Low: {pressure_info['pressure_low']} {pressure_info['unit']}")
    st.write(f"High: {pressure_info['pressure_high']} {pressure_info['unit']}")
    
    # Create a plotly figure for visualization
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=pressure_info['pressure'],
        title={'text': "Atmospheric Pressure"},
        delta={'reference': pressure_info['pressure_low']},
        gauge={
            'axis': {'range': [pressure_info['pressure_low'] - 10, pressure_info['pressure_high'] + 10]},
            'steps': [
                {'range': [pressure_info['pressure_low'], pressure_info['pressure']], 'color': "lightgray"},
                {'range': [pressure_info['pressure'], pressure_info['pressure_high']], 'color': "gray"}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': pressure_info['pressure_high']}
        }
    ))
    fig.update_layout(width=400, height=300)
    st.plotly_chart(fig)

# Function to create a card for humidity
def create_humidity_card(humidity_info):
    st.subheader(f"Date: {humidity_info['date']}")
    st.write(f"Humidity: {humidity_info['humidity']} {humidity_info['humidity_unit']}")

    # Create a bar chart for humidity visualization with enhanced styling
    humidity_df = pd.DataFrame({
        'Type': ['Current'],
        'Humidity': [humidity_info['humidity']]
    })

    fig = px.bar(humidity_df, x='Type', y='Humidity', title="Humidity", color='Type', 
                 color_discrete_map={'Current': 'green'})
    
    fig.update_traces(marker_line_color='black', marker_line_width=1.5, opacity=0.6)
    fig.update_layout(width=400, height=300, title_font_size=16, title_x=0.5, title_y=0.95)
    fig.update_yaxes(title_text='Humidity (%)')
    fig.update_xaxes(title_text='')
    
    st.plotly_chart(fig)

# Function to create a card for rain intensity
def create_rain_intensity_card(rain_info):
    st.subheader(f"Date: {rain_info['date']}")
    st.write(f"Rain Intensity: {rain_info['rain_intensity']} {rain_info['rain_unit']}")

    # Create a bar chart for rain intensity visualization with enhanced styling
    rain_df = pd.DataFrame({
        'Type': ['Current'],
        'Rain Intensity': [rain_info['rain_intensity']]
    })

    fig = px.bar(rain_df, x='Type', y='Rain Intensity', title="Rain Intensity", color='Type', 
                 color_discrete_map={'Current': 'blue'})
    
    fig.update_traces(marker_line_color='black', marker_line_width=1.5, opacity=0.6)
    fig.update_layout(width=400, height=300, title_font_size=16, title_x=0.5, title_y=0.95)
    fig.update_yaxes(title_text='Rain Intensity (mm/h)')
    fig.update_xaxes(title_text='')
    
    st.plotly_chart(fig)

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
    st.title("Flood Prediction")

    st.subheader("Latest IOT Data")
    # SQL query to fetch the first 10 records
    query = "SELECT * FROM iot_data ORDER BY created_at DESC LIMIT 1"
    iot_op_df = db.fetch_iot_output_data(query)
    # Exclude a specific column from the DataFrame
    columns_to_exclude = ['created_at', 'id','FloodProbability']
    latest_iot_data = iot_op_df.drop(columns=columns_to_exclude)
    if latest_iot_data is not None:
        st.dataframe(latest_iot_data)
    else:
        st.error("Failed to fetch Daily Report data from database")
    if st.button("Predict IOT Data"):
        # Call the prediction function
        prediction = predict_model(latest_iot_data)
        prediction_percent = prediction * 100
        if prediction>0.50:
            # sent alert to user
            send_email(prediction_percent)
        st.write("## IOT data Prediction Result")
        st.write(f"The predicted flood probability is: {prediction_percent:.2f}%")
    predict_sidebar_page()
    # Streamlit layout
    # Display the latest record
    col1, col2 = st.columns(2)

    with col1:
        create_pressure_card(latest_record)

    with col2:
        create_temperature_card(latest_record)

    col1, col2 = st.columns(2)

    with col1:
        create_humidity_card(latest_record)

    with col2:
        create_rain_intensity_card(latest_record)

def predict_sidebar_page():
    st.sidebar.subheader("Select the input values from below (range 0 to 20):")

    # Define the input fields
    fields = ["MonsoonIntensity", "TopographyDrainage", "RiverManagement", "Deforestation", "Urbanization", "ClimateChange", "DamsQuality", "Siltation", "AgriculturalPractices", "Encroachments", "IneffectiveDisasterPreparedness", "DrainageSystems", "CoastalVulnerability", "Landslides", "Watersheds", "DeterioratingInfrastructure", "PopulationScore", "WetlandLoss", "InadequatePlanning", "PoliticalFactors"]
    # Create input fields in the sidebar
    input_values = []
    for field in fields:
        value = st.sidebar.slider(f"{field}", 0, 20, 5)
        input_values.append(value)
    # Convert the input values to a DataFrame
    input_df = pd.DataFrame([input_values], columns=fields)
    if st.sidebar.button("Predict User Data"):
        # Call the prediction function
        prediction = predict_model(input_values)
        prediction_percent = prediction * 100
        if prediction>0.50:
            # sent alert to user
            send_email(prediction_percent)
        st.write("## User data Prediction Result")
        st.write(f"The predicted flood probability is: {prediction_percent:.2f}%")

def send_email(prediction_percent):
    to_address = "shivam.mahale9@gmail.com"
    subject = "Urgent: Flood Alert Notification"
    body = f"""
            <html>
            <body>
                <h4>Dear Resident,</h4>
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




    



