from datetime import datetime
import streamlit as st
import pandas as pd
import os
from dateutil.relativedelta import relativedelta

# Load the data to a dataframe
filepath = os.path.join(os.path.dirname(__file__), 'Dataset', 'Cleaned_HousePrice.csv')
df = pd.read_csv(filepath)

# Convert the PostedDate column to datetime
df['PostedDate'] = pd.to_datetime(df['PostedDate'], format='%d-%b-%Y', errors='coerce')

# WebScraping Results from Property Listing website
st.title("House Price Prediction Dataset-from Quicker")

# Filter Options
numberofbhk = st.sidebar.selectbox("Select NumberOfBHK:", ['All'] + sorted(df['NumberOfBHK'].unique().tolist()))
transaction = st.sidebar.selectbox("Select Transaction:", ['All'] + sorted(df['Transaction'].unique().tolist()))
availability = st.sidebar.selectbox("Select Availability:", ['All'] + sorted(df['Availability'].unique().tolist()))

# Date range filter
with st.sidebar:
    st.write("Posted Date Range Filter")
    col1, col2 = st.columns(2)

    with col1:
        startdate = st.date_input(
            "Start Date:",
            value=datetime.today() - relativedelta(months=2),
            label_visibility="collapsed"
        )
    with col2:
        enddate = st.date_input(
            "End Date:",
            value=datetime.today(),
            label_visibility="collapsed"
        )

# Convert startdate and enddate to datetime64
startdate = pd.to_datetime(startdate)
enddate = pd.to_datetime(enddate)

# Price range filter
with st.sidebar:
    st.write("Price Range Filter")
    col1, col2 = st.columns(2)

    with col1:
        pricemin = st.number_input(
            "Price Min:",
            value=df['Price'].astype(int).min(),
            label_visibility="collapsed"
        )
    with col2:
        pricemax = st.number_input(
            "Price Max:",
            value=df['Price'].astype(int).max(),
            label_visibility="collapsed"
        )

postedby = st.sidebar.selectbox("Select Posted By:", ['All'] + sorted(df['PostedBy'].unique().tolist()))
reraapproved = st.sidebar.selectbox("Select Rera Approved:", ['All'] + sorted(df['ReraApproved'].unique().tolist()))
areaname = st.sidebar.selectbox("Select Area Name:", ['All'] + sorted(df['AreaName'].unique().tolist()))

# Filter data based on user input
filtered_df = df[
    (df['PostedDate'] >= startdate) & (df['PostedDate'] <= enddate) &
    (df['Price'].astype(int) >= pricemin) & (df['Price'].astype(int) <= pricemax) &
    ((df['NumberOfBHK'] == numberofbhk) if numberofbhk != 'All' else True) &
    ((df['Transaction'] == transaction) if transaction != 'All' else True) &
    ((df['Availability'] == availability) if availability != 'All' else True) &
    ((df['PostedBy'] == postedby) if postedby != 'All' else True) &
    ((df['ReraApproved'] == reraapproved) if reraapproved != 'All' else True) &
    ((df['AreaName'] == areaname) if areaname != 'All' else True)
]

filtered_df = filtered_df.copy().reset_index(drop=True)

# Display the filtered data
st.dataframe(filtered_df)
