from mysql.connector import Error
import datetime
import mysql.connector
import streamlit as st
import hashlib
import pandas as pd
import re

# MySQL database connection details
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'flood_guard'
}

def get_db_connection():
    """Establish and return a connection to the MySQL database."""
    return mysql.connector.connect(**db_config)

def insert_user(email, username, password):
    """
    :param email:
    :param username:
    :param password:
    :return User on successful creation otherwise error:
    """
    date_joined = datetime.datetime.now()
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (email, username, password, date_joined) VALUES (%s, %s, %s, %s)",
            (email, username, password, date_joined)
        )
        conn.commit()
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()


def get_user(email):
    """Return a particular user if exists, else None."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def get_users():
    """Return a all user if exists, else None."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return users

def validate_username(username):
    """Check if a username is valid upon sign-up."""
    pattern = "^[a-zA-Z0-9-_]*$"
    return bool(re.match(pattern, username))

def validate_email(email):
    """Check if an email is valid."""
    pattern = r"^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    return bool(re.match(pattern, email))

def hash_password(password):
    """Hash a password for storing."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user."""
    return stored_password == hashlib.sha256(provided_password.encode()).hexdigest()
    
# Function to fetch data from MySQL and convert to Pandas DataFrame
def fetch_iot_output_data(query):
    connection = get_db_connection()
    if connection is not None and connection.is_connected():
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(rows, columns=columns)
            cursor.close()
            connection.close()
            return df
        except Error as e:
            print(f"The error '{e}' occurred")
            return None
        
# Function to create sample data
def get_geospatial_data():
    data = {
            'lat': [37.7749, 40.7128, 34.0522, 51.5074, 48.8566, 35.6895, 55.7558],
            'lon': [-122.4194, -74.0060, -118.2437, -0.1276, 2.3522, 139.6917, 37.6173],
            'location_name': ['San Francisco', 'New York City', 'Los Angeles', 'London', 'Paris', 'Tokyo', 'Moscow'],
            'weather_info': [
                'Sunny, 21°C', 
                'Cloudy, 18°C', 
                'Rainy, 15°C', 
                'Foggy, 10°C', 
                'Clear, 20°C',
                'Humid, 25°C',  
                'Snowy, -5°C'   
            ]
        }
    return pd.DataFrame(data)

def get_weather_data():

    weather_data = [
    {"date": "2024-06-24", "pressure": 1015, "temperature": 25, "pressure_low": 1010, "pressure_high": 1020, "temperature_low": 20, "temperature_high": 30, "unit": "hPa", "temp_unit": "°C", "rain_intensity": 2, "rain_unit": "mm/h", "humidity": 60, "humidity_unit": "%"},
    {"date": "2024-06-25", "pressure": 1017, "temperature": 26, "pressure_low": 1012, "pressure_high": 1022, "temperature_low": 21, "temperature_high": 31, "unit": "hPa", "temp_unit": "°C", "rain_intensity": 3, "rain_unit": "mm/h", "humidity": 65, "humidity_unit": "%"},
    {"date": "2024-06-26", "pressure": 1016, "temperature": 27, "pressure_low": 1011, "pressure_high": 1021, "temperature_low": 22, "temperature_high": 32, "unit": "hPa", "temp_unit": "°C", "rain_intensity": 1, "rain_unit": "mm/h", "humidity": 70, "humidity_unit": "%"},
    {"date": "2024-06-27", "pressure": 1018, "temperature": 28, "pressure_low": 1013, "pressure_high": 1023, "temperature_low": 23, "temperature_high": 33, "unit": "hPa", "temp_unit": "°C", "rain_intensity": 4, "rain_unit": "mm/h", "humidity": 75, "humidity_unit": "%"},
    {"date": "2024-06-28", "pressure": 1014, "temperature": 29, "pressure_low": 1009, "pressure_high": 1019, "temperature_low": 24, "temperature_high": 34, "unit": "hPa", "temp_unit": "°C", "rain_intensity": 0, "rain_unit": "mm/h", "humidity": 80, "humidity_unit": "%"},
]

    return weather_data;