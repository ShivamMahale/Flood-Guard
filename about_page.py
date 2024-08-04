import streamlit as st

def about_page():
    st.video("https://www.youtube.com/watch?v=HIFxkgfRy90")
    
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
