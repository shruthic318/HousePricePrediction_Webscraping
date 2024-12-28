from datetime import datetime
from matplotlib import pyplot as plt
import streamlit as st
import pandas as pd
import os
from dateutil.relativedelta import relativedelta

#Load the data to a dataframe
filepath = os.path.join(os.path.dirname(__file__), 'Dataset', 'Cleaned_HousePrice.csv')
df = pd.read_csv(filepath)
print(df.columns)

#WebScraping Results from Property Listing website
st.markdown("<h3 style='text-align: center; color: black;'>House Price Prediction Dataset-Quicker Property Listing</h3>", unsafe_allow_html=True)

#st.dataframe(df.head(5))

# Filter Options
numberofbhk = st.sidebar.selectbox("NumberOfBHK:",['All'] + sorted(df['NumberOfBHK'].unique().tolist()))
transaction = st.sidebar.selectbox("Transaction:",['All'] + sorted(df['Transaction'].unique().tolist()))
availability = st.sidebar.selectbox("Availability:",['All'] + sorted(df['Availability'].unique().tolist()))

df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
with st.sidebar:
    st.write("Price Range")
    col1, col2 = st.columns(2)

    with col1:
        pricemin = st.text_input(
            "PriceMin:",
            value=df['Price'].min(),
            label_visibility="collapsed" 
        )
        #st.caption("Start Date")
        pricemin = pd.to_numeric(pricemin, errors='coerce')
        if pd.isna(pricemin): 
            pricemin = df['Price'].min()

    with col2:
        pricemax = st.text_input(
            "PriceMax:",
            value=df['Price'].max(),
            label_visibility="collapsed"  
        )

        pricemax = pd.to_numeric(pricemax, errors='coerce')
        if pd.isna(pricemin): 
            pricemax = df['Price'].max()

with st.sidebar:
    st.write("Built Up Area Range")
    col1, col2 = st.columns(2)

    with col1:
        builtupareamin = st.text_input(
            "BuiltUpAreaMin:",
            value=df['BuiltUpArea_sqft'].min(),
            label_visibility="collapsed" 
        )
        #st.caption("Start Date")
        builtupareamin = pd.to_numeric(builtupareamin, errors='coerce')
        if pd.isna(builtupareamin): 
            builtupareamin = df['BuiltUpArea_sqft'].min()

    with col2:
        builtupareamax = st.text_input(
            "PriceMax:",
            value=df['BuiltUpArea_sqft'].max(),
            label_visibility="collapsed"  
        )

        builtupareamax = pd.to_numeric(builtupareamax, errors='coerce')
        if pd.isna(builtupareamax): 
            builtupareamax = df['BuiltUpArea_sqft'].max()

df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
df['BuiltUpArea_sqft'] = pd.to_numeric(df['BuiltUpArea_sqft'], errors='coerce')

postedby = st.sidebar.selectbox("Posted By:",['All']+ sorted(df['PostedBy'].unique().tolist()))
reraapproved = st.sidebar.selectbox("Rera Appproved:",['All']+ sorted(df['ReraApproved'].unique().tolist()))
areaname = st.sidebar.selectbox("Area Name:",['All']+sorted(df['AreaName'].unique().tolist()))
filtered_df = df[((df['Price'] >= pricemin) & (df['Price'] <= pricemax))
                & ((df['BuiltUpArea_sqft'] >= builtupareamin) & (df['BuiltUpArea_sqft'] <= builtupareamax))
                & ((df['NumberOfBHK'] == numberofbhk) if numberofbhk!='All' else True)
                & ((df['Transaction'] == transaction) if transaction!='All' else True)
                & ((df['Availability'] == availability) if availability!='All' else True)
                & ((df['PostedBy'] == postedby) if postedby!='All' else True)
                & ((df['ReraApproved'] == reraapproved) if reraapproved!='All' else True)
                & ((df['AreaName'] == areaname) if areaname!='All' else True)
                ]

filtered_df=filtered_df.iloc[:,1:]
st.dataframe(filtered_df)

import folium
from folium.plugins import MarkerCluster

# Load the CSV containing unique area names with latitude and longitude
filepath = os.path.join('Map','areas_latitude_longitude.csv')
area_coords = pd.read_csv(filepath)  


filtered_df['AreaName'] = filtered_df['AreaName'].str.strip().str.lower()
area_coords['AreaName'] = area_coords['AreaName'].str.strip().str.lower()

# Merge df with area_coords to get latitude and longitude for each AreaName
merged_df = pd.merge(filtered_df, area_coords, left_on="AreaName", right_on="AreaName", how="left")
#merged_df



# Initialize a Folium map centered on Bangalore
bangalore_map = folium.Map(location=[12.9716, 77.5946], zoom_start=10)

# Add markers to the map with MarkerCluster
marker_cluster = MarkerCluster().add_to(bangalore_map)

for _, row in merged_df.iterrows():
    # Ensure valid latitude and longitude
    if not pd.isnull(row['Latitude']) and not pd.isnull(row['Longitude']):
        # Create a popup with relevant information
        popup_html = f"""
        <b>Area:</b> {row['AreaName']}<br>
        <b>Number of BHK:</b> {row['NumberOfBHK']}<br>
        <b>Price:</b> {row['Price']}<br>
        <b>Transaction:</b> {row['Transaction']}<br>
        <b>Built-up Area:</b> {row['BuiltUpArea_sqft']}<br>
        <b>Availability:</b> {row['Availability']}<br>
        <b>Posted By:</b> {row['PostedBy']}<br>
        <b>RERA Approved:</b> {row['ReraApproved']}
        """
        
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=popup_html,
        ).add_to(marker_cluster)

# Display the map
st.markdown("<h3 style='text-align: center; color: black;'>Bangalore Map Visualization</h3>", unsafe_allow_html=True)
st.components.v1.html(bangalore_map._repr_html_(), height=600)

# Add a graph: Number of properties per area
st.markdown("<h3 style='text-align: center; color: black;'>Number of Properties per Area</h3>", unsafe_allow_html=True)
area_counts = filtered_df['AreaName'].value_counts()

fig, ax = plt.subplots(figsize=(10, 6))
area_counts.plot(kind='bar', ax=ax, color='skyblue')
ax.set_title('Number of Properties per Area', fontsize=16)
ax.set_xlabel('Area Name', fontsize=12)
ax.set_ylabel('Number of Properties', fontsize=12)
st.pyplot(fig)


# Save the map to an HTML file
#map_output_path = "bangalore_visualization_map.html"


#bangalore_map.save(map_output_path)

#print(f"Map saved to {map_output_path}. Open this file in a browser to view the visualization.")


