from datetime import datetime
import streamlit as st
import pandas as pd
import os
from dateutil.relativedelta import relativedelta

#Load the data to a dataframe
filepath = os.path.join('Dataset','HousePrice.csv')
df = pd.read_csv(filepath)  
#filepath = os.path.join(os.path.dirname(__file__), 'Dataset', 'HousePrice.csv')
#df = pd.read_csv(filepath)

#WebScraping Results from Property Listing website
st.title("House Price Prediction Dataset-from Quicker")

st.dataframe(df.head(5))

# Filter Options
numberofbhk = st.sidebar.selectbox("Select NumberOfBHK:", df['NumberOfBHK'].unique())
transaction = st.sidebar.selectbox("Select Transaction:", df['Transaction'].unique())
availability = st.sidebar.selectbox("Select Availability:", df['Availability'].unique())
with st.sidebar:
    st.write("Date Range Filter")
    col1, col2 = st.columns(2)

    with col1:
        startdate = st.date_input(
            "Start Date:",
            value=datetime.today() - relativedelta(months=2),
            label_visibility="collapsed" 
        )
        st.caption("Start Date")

    with col2:
        enddate = st.date_input(
            "End Date:",
            value=datetime.today(),
            label_visibility="collapsed"  
        )
        st.caption("End Date")

df['PostedDate'] = pd.to_datetime(df['PostedDate'], format='%d-%b-%Y')
#unique_dates = df['PostedDate'].dt.date.unique()
#date_filter = st.sidebar.selectbox('Date', unique_dates)
postedby = st.sidebar.selectbox("Select Posted By:", df['PostedBy'].unique())
reraapproved = st.sidebar.selectbox("Select Rera Appproved:", df['ReraApproved'].unique())
areaname = st.sidebar.selectbox("Select Area Name:", df['AreaName'].unique())
filtered_df = df[((df['PostedDate'].dt.date >= pd.to_datetime(startdate).date()) & (df['PostedDate'].dt.date <= pd.to_datetime(enddate).date())) 
                & (df['NumberOfBHK'] == numberofbhk)
                & (df['Transaction'] == transaction)
                & (df['Availability'] == availability)
                & (df['PostedBy'] == postedby)
                & (df['ReraApproved'] == reraapproved)
                & (df['AreaName'] == areaname)
                ]

st.write("Filtered Data:")
st.dataframe(filtered_df)
