import streamlit as st
import pandas as pd
import os

#Load the data to a dataframe
filepath = os.path.join('Dataset','HousePrice.csv')
df = pd.read_csv(filepath)  

#WebScraping Results from Property Listing website
st.title("House Price Prediction Dataset-from Quicker")

st.dataframe(df.head(5))

# Filter Options
numberofbhk = st.sidebar.selectbox("Select NumberOfBHK:", df['NumberOfBHK'].unique())
transaction = st.sidebar.selectbox("Select Transaction:", df['Transaction'].unique())
availability = st.sidebar.selectbox("Select Availability:", df['Availability'].unique())
date = st.date_input("Select Posted Date:")
df['PostedDate'] = pd.to_datetime(df['PostedDate'], format='%Y-%m-%d %H:%M:%S')
unique_dates = df['last_updated'].dt.date.unique()
date_filter = st.sidebar.selectbox('Date', unique_dates)
postedby = st.sidebar.selectbox("Select Posted By:", df['PostedBy'].unique())
reraapproved = st.sidebar.selectbox("Select Rera Appproved:", df['ReraApproved'].unique())
areaname = st.sidebar.selectbox("Select Area Name:", df['AreaName'].unique())
filtered_df = df[(df['PostedDate'].dt.date == pd.to_datetime(date_filter).date()) 
                & (df['NumberOfBHK'] == numberofbhk)
                & (df['Transaction'] == transaction)
                & (df['Availability'] == availability)
                & (df['PostedBy'] == postedby)
                & (df['ReraApproved'] == reraapproved)
                & (df['AreaName'] == areaname)
                ]

st.write("Filtered Data:")
st.dataframe(filtered_df)
