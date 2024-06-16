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
    st.title("Contact Us")
    st.subheader("We'd love to hear from you!")

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
