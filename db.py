import datetime
import mysql.connector
import streamlit as st
import hashlib
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
    