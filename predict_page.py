import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
import plotly.graph_objs as go
import plotly.express as px
import db

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
    st.subheader("Enter the input values for prediction (range 0 to 20):")

    # Define the input fields
    fields = ["MonsoonIntensity", "TopographyDrainage", "RiverManagement", "Deforestation", "Urbanization", "ClimateChange", "DamsQuality", "Siltation", "AgriculturalPractices", "Encroachments", "IneffectiveDisasterPreparedness", "DrainageSystems", "CoastalVulnerability", "Landslides", "Watersheds", "DeterioratingInfrastructure", "PopulationScore", "WetlandLoss", "InadequatePlanning", "PoliticalFactors"]
    # Create input fields in the sidebar
    input_values = []
    for field in fields:
        value = st.sidebar.slider(f"{field}", 0, 20, 5)
        input_values.append(value)
    # Convert the input values to a DataFrame
    input_df = pd.DataFrame([input_values], columns=fields)
    if st.button("Predict"):
        # Call the prediction function
        prediction = predict_model(input_values)
        
        st.write("## Prediction Result")
        st.write(f"The predicted flood probability is: {prediction}")


    # Streamlit layout
    # Display the latest record
    col1, col2 = st.columns(2)

    with col1:
        create_pressure_card(latest_record)

    with col2:
        create_temperature_card(latest_record)

    



