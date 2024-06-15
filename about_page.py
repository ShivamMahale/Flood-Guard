import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

def about_page():
    st.video("https://www.youtube.com/watch?v=HIFxkgfRy90")
    st.write("""
    FloodGuard is your ultimate solution for staying ahead of potential flood risks and ensuring the safety of your community. 
    With advanced prediction algorithms and real-time monitoring capabilities, FloodGuard provides accurate forecasts 
    and timely alerts to help you prepare and respond effectively to flood events.

    **Key Features:**

    1. **Accurate Prediction**: Our sophisticated prediction models leverage historical data, weather patterns, and river levels to forecast potential flood events with high accuracy.

    2. **Real-Time Monitoring**: Stay informed with real-time updates on weather conditions, river levels, and flood risks in your area, empowering you to make informed decisions quickly.

    3. **Customized Alerts**: Receive personalized alerts via email, SMS, or mobile notifications, tailored to your location and specific flood risk thresholds.

    4. **Interactive Maps**: Explore interactive maps that visualize flood-prone areas, evacuation routes, and emergency shelters, helping you plan and navigate during flood emergencies.

    5. **Community Engagement**: Connect with your local community and authorities through our platform to share information, report incidents, and coordinate response efforts.

    **Why Choose FloodGuard?**

    - **Proactive Protection**: Be proactive in mitigating flood risks and protecting lives and property with our advanced warning system.
    - **Reliable Information**: Trust in our reliable and up-to-date data sources and expert analysis to guide your flood preparedness and response strategies.
    - **Peace of Mind**: Gain peace of mind knowing that you're equipped with the latest tools and information to face flood challenges confidently.

    **Get Started Today**

    Don't wait for the next flood event to act. Sign up for FloodGuard now and take control of your flood preparedness journey. Together, we can build a safer and more resilient community.
    """)

    # Add a sample visualization
    st.header("Sample Visualization")
    # Create sample dataframe
    np.random.seed(0)
    data = pd.DataFrame({
        'Date': pd.date_range(start='2022-01-01', end='2022-12-31', freq='D'),
        'Temperature': np.random.uniform(low=0, high=30, size=(365,))
    })

    # Create line chart using Altair
    line_chart = alt.Chart(data).mark_line().encode(
        x='Date',
        y='Temperature',
    ).properties(
        width=600,
        height=300
    )

    # Display line chart
    st.altair_chart(line_chart, use_container_width=True)
