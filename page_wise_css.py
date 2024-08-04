import streamlit as st
import base64
import plotly.express as px


def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


def get_sidebar_style(img):
    page_bg_img = f"""
    <style>

    [data-testid="stSidebar"] > div:first-child {{
    background-image: url("data:image/png;base64,{img}");
    background-position: center; 
    background-attachment: fixed;
    width: 400px;  # Set the sidebar width
    }}

    [data-testid="stSidebar"] * {{
    font-size: 20px;  # Increase font size for all sidebar content
    color: #000000;  # Ensure text color is light
    }}

    [data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
    }}

    [data-testid="stToolbar"] {{
    right: 2rem;
    }}
    </style>
    """

    return page_bg_img;

def get_page_style(img):
    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
    background-image: url("data:image/png;base64,{img}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;

    }}

    [data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
    }}

    [data-testid="stToolbar"] {{
    right: 2rem;
    }}
    </style>
    """

    return page_bg_img;