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
    validated = False
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (email, username, password, date_joined, validated) VALUES (%s, %s, %s, %s, %s)",
            (email, username, password, date_joined, validated)
        )
        conn.commit()
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

def fetch_users_emails():
    """Fetch user emails and return them as a list."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM users")
    emails = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return emails

def fetch_usernames():
    """Fetch all usernames in the database and return them as a list."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users")
    usernames = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return usernames

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
    pattern = "^[a-z]*$"
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

def sign_up():
    with st.form(key='signup', clear_on_submit=False):
        st.subheader('Sign up')
        email = st.text_input('Email', placeholder='Enter email')
        username = st.text_input('Username', placeholder='Enter Username')
        password = st.text_input('Password', placeholder='Enter password', type='password')
        password2 = st.text_input('Password', placeholder='Confirm password', type='password')

        if email:
            if validate_email(email):
                if email not in fetch_users_emails():
                    if validate_username(username):
                        if len(username) >= 2:
                            if username not in fetch_usernames():
                                if len(password) >= 6:
                                    if password == password2:
                                        hashed_password = hash_password(password)
                                        insert_user(email=email, username=username, password=hashed_password)
                                        st.success('Account created Successfully')
                                        st.balloons()
                                    else:
                                        st.warning('Passwords do not match')
                                else:
                                    st.warning('Password should be at least 6 characters')
                            else:
                                st.warning('Username Already Exists')
                        else:
                            st.warning('Username too short')
                    else:
                        st.warning('Invalid characters in Username')
                else:
                    st.warning('Email Already Exists!!')
            else:
                st.warning('Invalid email Address')

        col1, col2, col3, col4, col5 = st.columns(5)
        with col3:
            st.form_submit_button('Sign up')

def login():
    with st.form(key='login', clear_on_submit=False):
        st.subheader('Login')
        email = st.text_input('Email', placeholder='Enter email')
        password = st.text_input('Password', placeholder='Enter password', type='password')
        if email:
            if validate_email(email):
                if email in fetch_users_emails():
                    user = get_user(email)
                    if user and verify_password(user['password'], password):
                        st.session_state.login_success = True
                        st.session_state.user_name = user['username']
                        st.success('Logged in successfully!')
                    else:
                        st.warning('Invalid email or password')
                else:
                    st.warning('Email Does Not Exist. Please Sign up')
            else:
                st.warning('Invalid Email Address')

        col1, col2, col3, col4, col5 = st.columns(5)
        with col3:
            st.form_submit_button('Login')



