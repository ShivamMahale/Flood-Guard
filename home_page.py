import io
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import db
import pydeck as pdk
import matplotlib.pyplot as plt
import seaborn as sns

# Define a styling function
def highlight_max(s):
    '''
    highlight the maximum in a Series yellow.
    '''
    is_max = s == s.max()
    return ['background-color: yellow' if v else '' for v in is_max]

def highlight_min(s):
    '''
    highlight the minimum in a Series lightblue.
    '''
    is_min = s == s.min()
    return ['background-color: lightblue' if v else '' for v in is_min]

def home_page():
    st.write("""
    FloodGuard is your ultimate solution for staying ahead of potential flood risks and ensuring the safety of your community. 
    With advanced prediction algorithms and real-time monitoring capabilities, FloodGuard provides accurate forecasts 
    and timely alerts to help you prepare and respond effectively to flood events.
    """)

    # Add a daily report visualization
    st.subheader("Daily Report based upon IOT Data receiving from selected Area")
    # SQL query to fetch the first 10 records
    query = "SELECT * FROM iot_data ORDER BY created_at DESC LIMIT 10"
    iot_op_df = db.fetch_iot_output_data(query)
    # Exclude a specific column from the DataFrame
    columns_to_exclude = ['created_at', 'id']
    iot_op_df_with_no_date = iot_op_df.drop(columns=columns_to_exclude)
    if iot_op_df is not None:
        st.dataframe(iot_op_df)
        # Print DataFrame info
        st.subheader("Real Time IOT data statistical analysis")
        st.write(iot_op_df_with_no_date.describe())
    else:
        st.error("Failed to fetch Daily Report data from database")

    st.subheader('Flood Probability Distribution')

    # Create line chart using Altair
    line_chart = alt.Chart(iot_op_df).mark_line().encode(
        x='id',
        y='FloodProbability',
    ).properties(
        width=600,
        height=300
    )

    # Display line chart
    st.altair_chart(line_chart, use_container_width=True)

    # Plotting using matplotlib and seaborn
    plt.figure(figsize=(10, 6))
    sns.histplot(iot_op_df['FloodProbability'], bins=20, kde=True)
    plt.title('Distribution of FloodProbability')
    plt.xlabel('FloodProbability')
    plt.ylabel('Count')

    # Display the plot in Streamlit
    st.pyplot()


    # display plot of each column
    st.subheader('Analysis of Each Attribute')


    columns_to_exclude = ['created_at', 'id','FloodProbability']
    df_for_all_column_plot = iot_op_df.drop(columns=columns_to_exclude)

    # Number of columns to display per row
    columns_per_row = 4
    cols = df_for_all_column_plot.columns.tolist()
    # Loop through each column and create histograms
    for i in range(0, len(cols), columns_per_row):
        fig, axs = plt.subplots(1, columns_per_row, figsize=(20, 5))
        for j, col in enumerate(cols[i:i + columns_per_row]):
            max_val = round(df_for_all_column_plot[col].max()) + 1
            df_for_all_column_plot[col].hist(density=True, bins=np.arange(0, max_val, 1), ax=axs[j])
            axs[j].set_xticks(np.arange(0, 10, 1))
            axs[j].set_title(col)
            axs[j].set_xlabel(col)
            axs[j].set_ylabel('Density')

        # Display the plot in Streamlit
        st.pyplot(fig)



    # Fetch geo spatial data
    df = db.get_geospatial_data()
    st.subheader("Global Map")

    # Display the map with weather information
    if df is not None and not df.empty:
        layer = pdk.Layer(
            'ScatterplotLayer',
            df,
            get_position='[lon, lat]',
            get_color='[200, 30, 0, 160]',
            get_radius=200000,
            pickable=True,
            auto_highlight=True
        )
        # Define the pydeck view
        view_state = pdk.ViewState(
            latitude=37.7749,
            longitude=-122.4194,
            zoom=2,  # Set initial zoom level
            pitch=0,  # Set initial pitch for a more 2D view
            bearing=0
        )
        # Create the pydeck deck.gl map
        deck = pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip={"text": "{location_name}\n{weather_info}\n(lat: {lat}, lon: {lon})"},
            map_style='mapbox://styles/mapbox/light-v10',  # You can use different map styles
            views=[pdk.View(type="MapView", controller=True)]  # Enable map controls
        )

        # Display the pydeck map
        st.pydeck_chart(deck)
        
    else:
        st.error("Failed to fetch data")
    