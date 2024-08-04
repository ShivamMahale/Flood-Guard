import streamlit as st
import db
import page_wise_css as pwcss


st.set_page_config(
        page_title="FloodGuard: Flood Prediction and Early Warning System",
        page_icon=":material/dashboard:",
        layout="wide",
        initial_sidebar_state="expanded",
    )

dialog_style = """
    <style>
        .stDialog {
            width: 600px;
            height: 500px;
            padding: 30px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 20px;
            color: white;
        }
        .stDialog h1, .stDialog h2, .stDialog h3, .stDialog h4, .stDialog h5, .stDialog h6 {
            color: white;
        }
        .stDialog input {
            color: black;
        }
        .dialog-content {
            text-align: center;
        }
        .dialog-icon {
            margin-bottom: 20px;
            font-size: 70px; /* Adjust size of the icon */
        }
    </style>
"""


home_img = pwcss.get_img_as_base64("./images/fllod.jpg")
side_img = pwcss.get_img_as_base64("./images/cloud.jpg")
sidebar_style=pwcss.get_sidebar_style(side_img)
st.markdown(sidebar_style, unsafe_allow_html=True)

def display_vision_statement():
    st.markdown("""
        <style>
            .vision-container {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 60vh; /* Full viewport height */
            }
            .vision-statement {
                background-color: rgba(0, 68, 102, 0.7); /* Background color with transparency */
                color: #FFFFFF; /* Text color */
                padding: 40px;
                border-radius: 20px;
                text-align: center;
                font-family: 'Georgia', serif;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                max-width: 800px;
                width: 100%;
            }
            .vision-title {
                font-size: 36px;
                font-weight: bold;
                margin-bottom: 20px;
            }
            .vision-description {
                font-size: 22px;
                line-height: 1.5;
                margin-bottom: 20px;
            }
            .vision-icon {
                font-size: 50px;
                margin-bottom: 20px;
            }
        </style>
        <div class="vision-container">
            <div class="vision-statement">
                <div class="vision-icon">🌊</div>
                <div class="vision-title">Empowering Communities with Flood Resilience</div>
                <div class="vision-description">
                    "To empower communities worldwide with advanced flood prediction and early warning systems, ensuring safety, preparedness, and resilience against natural disasters."
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Function to handle signup
@st.experimental_dialog("Welcome to FloodGuard ! Please Signup")
def signup():
    st.markdown(dialog_style, unsafe_allow_html=True)
    st.markdown("""
        <div class="dialog-content">
            <div class="dialog-icon">
                🌊
            </div>
            <h2>Your Comprehensive Flood Prediction and Early Warning System</h2>
            <p style="font-size: 16px;">Please enter your details to signup.</p>
        </div>
    """, unsafe_allow_html=True)
    email = st.text_input('Email', placeholder='Enter email')
    username = st.text_input('Username', placeholder='Enter Username')
    password = st.text_input("Password", placeholder='Enter password',type="password")

    if st.button("Signup", key="signup_button"):
        if db.validate_email(email):
            user = db.get_user(email)
            if user is not None:
                st.warning("Username already exists. Please choose another one.")
            else:
                if db.validate_username(username):
                    if len(username) >= 2:
                        if len(password) >= 6:
                            hashed_password = db.hash_password(password)
                            db.insert_user(email=email, username=username, password=hashed_password)
                            st.success("User registered successfully! Please login.")
                            st.session_state.signup = False
                            st.session_state.logged_in = False
                            st.experimental_rerun()  # Force rerun
                        else:
                            st.warning('Password should be at least 6 characters')
                    else:
                        st.warning('Username too short')
                else:
                    st.warning('Invalid characters in Username')
        else:
            st.warning('Invalid email Address')
        
# Function to handle login
@st.experimental_dialog("Welcome to FloodGuard ! Please Login")
def login():
    st.markdown(dialog_style, unsafe_allow_html=True)
    st.markdown("""
        <div class="dialog-content">
            <div class="dialog-icon">
                🌊
            </div>
            <h2>Your Comprehensive Flood Prediction and Early Warning System</h2>
            <p style="font-size: 16px;">Please enter your email and password to login.</p>
        </div>
    """, unsafe_allow_html=True)

    
    email = st.text_input("Email",placeholder="Enter your registered email id")
    password = st.text_input("Password", type="password",placeholder="Enter your password")
    if st.button("Login", key="login_button"):
        user = db.get_user(email)
        if user and db.verify_password(user['password'],password):
            st.session_state.logged_in = True
            st.session_state.username = user['username']
            st.success("Logged in successfully")
            st.experimental_rerun()  # Force rerun
        else:
            st.error("Invalid username or password")

# Function to handle logout
def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.signup = False
    st.experimental_rerun()  # Force rerun

# Function to render page content based on selection
def render_page(page):
    if page == "Dashboard":
        from home_page import home_page
        home_page()
    elif page == "Weather Lens":
        from forcast import forcast_page
        forcast_page()
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

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.signup = False

    if st.session_state.logged_in:
        # Sidebar navigation
        st.sidebar.title(f"Welcome, {st.session_state.username}!")
        
        page = st.sidebar.radio("Menu", ["Dashboard", "Weather Lens","About", "Prediction","Contact"])
        

        # Logout button
        if st.sidebar.button("Logout", key="sidebar_logout"):
            logout()

        # Render selected page content
        render_page(page)
    else:
        st.title("Welcome to FloodGuard!")
        display_vision_statement()
        st.sidebar.title("Account")
        pg_style=pwcss.get_page_style(home_img)
        st.markdown(pg_style, unsafe_allow_html=True)
        if st.sidebar.button("Signup", key="sidebar_signup"):
            st.session_state.signup = True
            st.session_state.logged_in = False
            st.experimental_rerun()  # Force rerun
        if st.sidebar.button("Login", key="sidebar_login"):
            st.session_state.signup = False
            st.session_state.logged_in = False
            st.experimental_rerun()  # Force rerun

        if st.session_state.signup:
            signup()
        else:
            login()

# Run the main application
if __name__ == "__main__":
    main()
