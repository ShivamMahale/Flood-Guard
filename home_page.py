
import streamlit as st
import db
import pydeck as pdk
import seaborn as sns
import plotly.express as px

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
    st.write('<p style="font-size: 20px; color: white;">FloodGuard is your ultimate solution for staying ahead of potential flood risks and ensuring the safety of your community.With advanced prediction algorithms and real-time monitoring capabilities, FloodGuard provides accurate forecasts and timely alerts to help you prepare and respond effectively to flood events.</p>', unsafe_allow_html=True)

    # SQL query to fetch the first 10 records
    query = "SELECT * FROM iot_data ORDER BY created_at DESC LIMIT 10"
    iot_op_df = db.fetch_iot_output_data(query)
    # Exclude a specific column from the DataFrame
    columns_to_exclude = ['created_at', 'id']
    iot_op_df_with_no_date = iot_op_df.drop(columns=columns_to_exclude)
    
    if iot_op_df is not None:
        
        # Visualizing Flood Probability
        st.subheader('Flood Probability Distribution')
        fig_flood_prob = px.histogram(iot_op_df, x='FloodProbability', nbins=20, title='Flood Probability Distribution')
        fig_flood_prob.update_layout(width=900)  # Increase the width of the histogram
        st.plotly_chart(fig_flood_prob)


        # Add interactive scatter plots for all columns, two per row
        columns_to_plot = iot_op_df.columns.drop(['created_at', 'id', 'FloodProbability'])
        color_schemes = px.colors.qualitative.Set1

        for i in range(0, len(columns_to_plot), 2):
            col1, col2 = st.columns(2)
            
            if i < len(columns_to_plot):
                with col1:
                    st.subheader(f'{columns_to_plot[i]} vs Flood Probability Scatter Plot')
                    fig_scatter1 = px.scatter(iot_op_df, x=columns_to_plot[i], y='FloodProbability', 
                                              color='FloodProbability', title=f'{columns_to_plot[i]} vs Flood Probability',
                                              color_continuous_scale=color_schemes)
                    fig_scatter1.update_traces(marker=dict(size=10, line=dict(width=2, color='DarkSlateGrey')),
                                               selector=dict(mode='markers'))
                    fig_scatter1.update_layout(width=400, height=400)
                    st.plotly_chart(fig_scatter1)
            
            if i + 1 < len(columns_to_plot):
                with col2:
                    st.subheader(f'{columns_to_plot[i + 1]} vs Flood Probability Scatter Plot')
                    fig_scatter2 = px.scatter(iot_op_df, x=columns_to_plot[i + 1], y='FloodProbability', 
                                              color='FloodProbability', title=f'{columns_to_plot[i + 1]} vs Flood Probability',
                                              color_continuous_scale=color_schemes)
                    fig_scatter2.update_traces(marker=dict(size=10, line=dict(width=2, color='DarkSlateGrey')),
                                               selector=dict(mode='markers'))
                    fig_scatter2.update_layout(width=400, height=400)
                    st.plotly_chart(fig_scatter2)
            
            st.markdown("<hr style='border:2px solid white;'>", unsafe_allow_html=True)

             # Add a daily report visualization
        st.subheader("Daily Report based upon IOT Data receiving from selected Area")
        st.dataframe(iot_op_df)

        # Print DataFrame info
        st.subheader("Real Time IOT data statistical analysis")
        st.write(iot_op_df_with_no_date.describe())
                    
    else:
        st.error("Failed to fetch Daily Report data from database")



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
    