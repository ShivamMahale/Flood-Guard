import streamlit as st
from db import get_db_connection



# Function to insert contact information into the database
def insert_contact(connection, name, email, message):
    cursor = connection.cursor()
    query = "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)"
    values = (name, email, message)
    cursor.execute(query, values)
    connection.commit()
    cursor.close()


# Contact form
def contact_page():
    # Include Font Awesome CDN
    st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">', unsafe_allow_html=True)

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
            background-image: url('https://images.pexels.com/photos/3783229/pexels-photo-3783229.jpeg?auto=compress&cs=tinysrgb&w=600');
            background-size: cover;
            background-position: center;
            padding: 12rem;
            margin-top: 1rem;
            margin-bottom: 1rem;
        }
        .centered-title {
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="centered-title">How can we help at FloodGuard 🌊</h1>', unsafe_allow_html=True)
    st.markdown('<div class="background-image">', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">We are here to answer your questions and assist you with any inquiries or concerns. Reach out to us below!</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    

    st.markdown('<h1 class="centered-title">Contact Us <i class="fas fa-envelope"></i></h1>', unsafe_allow_html=True)


    name = st.text_input("Name", placeholder="Enter your name")
    email = st.text_input("Email", placeholder="Enter your email")
    message = st.text_area("Message", placeholder="Enter your message")

    if st.button("Submit"):
        if name and email and message:
            connection = get_db_connection()
            if connection:
                insert_contact(connection, name, email, message)
                st.success("Your message has been sent successfully!")
                connection.close()
        else:
            st.error("Please fill out all fields")
