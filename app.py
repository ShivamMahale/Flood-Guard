import streamlit as st
import hashlib

# Helper functions to hash passwords and check them
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(password, hashed):
    return hash_password(password) == hashed

# Sample user database - In real-world applications, use a proper database
user_db = {"Bachan": hash_password("admin123")}

# Function to handle signup
def signup():
    st.title("Welcome to FloodGuard")
    st.subheader("Your Comprehensive Flood Prediction and Early Warning System")
    st.subheader("Signup")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Signup", key="signup_button"):
        if username in user_db:
            st.warning("Username already exists. Please choose another one.")
        else:
            user_db[username] = hash_password(password)
            st.success("User registered successfully! Please login.")
            st.session_state.signup = False
            st.session_state.logged_in = False
            st.rerun()  # Force rerun

# Function to handle login
def login():
    st.title("Welcome to FloodGuard")
    st.subheader("Your Comprehensive Flood Prediction and Early Warning System")
    st.subheader("Login")
    username = st.text_input("Username",placeholder="Enter your username")
    password = st.text_input("Password", type="password",placeholder="Enter your password")
    if st.button("Login", key="login_button"):
        if username in user_db and check_password(password, user_db[username]):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()  # Force rerun
        else:
            st.error("Invalid username or password")

# Function to handle logout
def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.signup = False
    st.rerun()  # Force rerun

# Function to render page content based on selection
def render_page(page):
    if page == "Home":
        from about_page import about_page
        about_page()
    elif page == "About":
        from about_page import about_page
        about_page()
    elif page == "Prediction":
        from predict_page import predict_page
        predict_page()
    elif page == "Contact":
        from contact_page import contact_page
        contact_page()

# Main application
def main():
    st.set_page_config(
        page_title="FloodGuard: Flood Prediction and Early Warning System",
        page_icon="🌊",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.signup = False

    if st.session_state.logged_in:
        st.title("Welcome to FloodGuard")
        st.subheader("Your Comprehensive Flood Prediction and Early Warning System")

        # Sidebar navigation
        st.sidebar.title(f"Welcome, {st.session_state.username}!")
        page = st.sidebar.radio("Menu", ["Home", "About", "Prediction","Contact"])

        # Logout button
        if st.sidebar.button("Logout", key="sidebar_logout"):
            logout()

        # Render selected page content
        render_page(page)
    else:
        st.sidebar.title("Account")
        if st.sidebar.button("Signup", key="sidebar_signup"):
            st.session_state.signup = True
            st.session_state.logged_in = False
            st.rerun()  # Force rerun
        if st.sidebar.button("Login", key="sidebar_login"):
            st.session_state.signup = False
            st.session_state.logged_in = False
            st.rerun()  # Force rerun

        if st.session_state.signup:
            signup()
        else:
            login()

# Run the main application
if __name__ == "__main__":
    main()
