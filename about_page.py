import streamlit as st

def about_page():
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
            background-image: url('https://images.pexels.com/photos/6802048/pexels-photo-6802048.jpeg?auto=compress&cs=tinysrgb&w=600');
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

    st.markdown('<h1 class="centered-title">About FloodGuard 🌊</h1>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Your Comprehensive Flood Prediction and Early Warning System',unsafe_allow_html=True)
    st.markdown('<div class="background-image">', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Explore global weather patterns and their impact on flood risks with our early warning FloodGuard portal.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<hr>', unsafe_allow_html=True)

    video_url = "https://www.youtube.com/embed/HIFxkgfRy90"

    st.markdown("""
    <style>
    .custom-text {
        font-size: 20px; /* Change this value to your desired font size */
        color: white; /* Change this value to your desired text color */
    }
    </style>
    <div class="custom-text">
    FloodGuard is your ultimate solution for staying ahead of potential flood risks and ensuring the safety of your community. 
    With advanced prediction algorithms and real-time monitoring capabilities, FloodGuard provides accurate forecasts 
    and timely alerts to help you prepare and respond effectively to flood events.
    </div>
    """, unsafe_allow_html=True)

    # Define the custom HTML and CSS for embedding the video
    video_html = f"""
        <div style="display: flex; justify-content: center;">
            <iframe width="1000" height="350" src="{video_url}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        </div>
    """
    st.markdown("""<br></br>""",unsafe_allow_html=True)
    # Display the video
    st.markdown(video_html, unsafe_allow_html=True)
    st.markdown("""<br></br>""",unsafe_allow_html=True)
    st.markdown("""
    <style>
    .custom-text {
        font-size: 20px; /* Change this value to your desired font size */
        color: white; /* Change this value to your desired text color */
    }
    </style>
    <div class="custom-text">

    <b>Key Features:</b>

    1. <b>Accurate Prediction</b>: Our sophisticated prediction models leverage historical data, weather patterns, and river levels to forecast potential flood events with high accuracy.

    2. <b>Real-Time Monitoring</b>: Stay informed with real-time updates on weather conditions, river levels, and flood risks in your area, empowering you to make informed decisions quickly.

    3. <b>Customized Alerts</b>: Receive personalized alerts via email, SMS, or mobile notifications, tailored to your location and specific flood risk thresholds.

    4. <b>Interactive Maps</b>: Explore interactive maps that visualize flood-prone areas, evacuation routes, and emergency shelters, helping you plan and navigate during flood emergencies.

    5. <b>Community Engagement</b>: Connect with your local community and authorities through our platform to share information, report incidents, and coordinate response efforts.

    <b>Why Choose FloodGuard?</b>

    - <b>Proactive Protection</b>: Be proactive in mitigating flood risks and protecting lives and property with our advanced warning system.
    - <b>Reliable Information</b>: Trust in our reliable and up-to-date data sources and expert analysis to guide your flood preparedness and response strategies.
    - <b>Peace of Mind</b>: Gain peace of mind knowing that you're equipped with the latest tools and information to face flood challenges confidently.

    <b>Get Started Today</b>

    Don't wait for the next flood event to act. Sign up for FloodGuard now and take control of your flood preparedness journey. Together, we can build a safer and more resilient community.
    </div>
    """, unsafe_allow_html=True)
