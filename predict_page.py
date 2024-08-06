import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
import db
import notification
from streamlit.components.v1 import html

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
    location_name = st.text_input("Enter location (e.g., London, New York)")
    st.markdown('</div>', unsafe_allow_html=True)
    fetch_button = st.button("Fetch IOT Data",key="fetch")
    if fetch_button and location_name:
        st.session_state['iot_data_fetched'] = True
    if 'iot_data_fetched' in st.session_state and st.session_state['iot_data_fetched']:
        predict_iot_data()

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
def predict_iot_data():
        # SQL query to fetch the first 10 records
        query = "SELECT * FROM iot_data ORDER BY RAND() LIMIT 1"
        iot_op_df = db.fetch_iot_output_data(query)
        # Exclude a specific column from the DataFrame
        columns_to_exclude = ['created_at', 'id','FloodProbability']
        latest_iot_data = iot_op_df.drop(columns=columns_to_exclude)
        if latest_iot_data is not None:
            st.dataframe(latest_iot_data)
        else:
            st.error("Failed to fetch Daily Report data from database")
        st.markdown('<div class="sub-title">Click on the prediction button to predict probability of flood for the below latest IOT Data</div>', unsafe_allow_html=True)
        if st.button("Predict IOT Data",key="predict"):
            # Call the prediction function
            prediction = predict_model(latest_iot_data)
            prediction_percent = prediction * 100
            if prediction>0.50:
                # sent alert to user
                send_email(prediction_percent)
            display_prediction_card(prediction_percent,"IOT")

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




    



