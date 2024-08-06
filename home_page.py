
import streamlit as st
import db
import pydeck as pdk
import plotly.express as px
import pandas as pd
def home_page():
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
    .background-image {
            background-image: url('https://images.pexels.com/photos/3183153/pexels-photo-3183153.jpeg?auto=compress&cs=tinysrgb&w=600');
            background-size: cover;
            background-position: center;
            padding: 15rem;
            margin-top: 1rem;
            margin-bottom: 2rem;
        }
        .centered-title {
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)
    st.markdown("""
    <div class="main-title">
        IOT Data Dashboard <i class="fas fa-chart-line"></i>
    </div>
    <div class="sub-title">
        Monitor and analyze real-time data trends with our intuitive dashboard.
    </div>
""", unsafe_allow_html=True)

    st.markdown('<div class="background-image">', unsafe_allow_html=True)

    # Section 2
    with st.expander("IOT Data Visualization", expanded=False):

        st.markdown('<div class="main-title">IOT Data Visualization</div>', unsafe_allow_html=True)
        # SQL query to fetch the first 10 records
        query = "SELECT * FROM iot_data ORDER BY created_at DESC LIMIT 10"
        iot_op_df = db.fetch_iot_output_data(query)
        # Exclude a specific column from the DataFrame
        columns_to_exclude = ['created_at', 'id']
        iot_op_df_with_no_date = iot_op_df.drop(columns=columns_to_exclude)
        # Visualizing Flood Probability

        fig_flood_prob = px.histogram(iot_op_df, x='FloodProbability', nbins=20, title='Flood Probability Distribution')
        fig_flood_prob.update_layout(width=850,title_x=0.6,title_xanchor='center')  # Increase the width of the histogram
        fig_flood_prob.update_layout(height=500)  # Set fixed height
        st.plotly_chart(fig_flood_prob)
        
        if iot_op_df is not None:

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
                        fig_scatter1.update_layout(width=400, height=400,title_x=0.5,title_xanchor='center')
                        st.plotly_chart(fig_scatter1)
                
                if i + 1 < len(columns_to_plot):
                    with col2:
                        st.subheader(f'{columns_to_plot[i + 1]} vs Flood Probability Scatter Plot')
                        fig_scatter2 = px.scatter(iot_op_df, x=columns_to_plot[i + 1], y='FloodProbability', 
                                                color='FloodProbability', title=f'{columns_to_plot[i + 1]} vs Flood Probability',
                                                color_continuous_scale=color_schemes)
                        fig_scatter2.update_traces(marker=dict(size=10, line=dict(width=2, color='DarkSlateGrey')),
                                                selector=dict(mode='markers'))
                        fig_scatter2.update_layout(width=400, height=400,title_x=0.5,title_xanchor='center')
                        st.plotly_chart(fig_scatter2)
                
                st.markdown("<hr style='border:2px solid white;'>", unsafe_allow_html=True)

                # Add a daily report visualization
            
            st.subheader("Daily Report based upon IOT Data receiving from selected Area")
            st.dataframe(
            iot_op_df,
            column_config={"Year": st.column_config.NumberColumn(format="%d")},
        )
                        
        else:
            st.error("Failed to fetch Daily Report data from database")

    #Map Section
    with st.expander("Weather Visualization on Global Map", expanded=False):
        st.subheader('Weather Visualization on Global Map')
        # Fetch geo spatial data
        df = db.get_geospatial_data()

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
    