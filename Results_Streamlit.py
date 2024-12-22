from datetime import datetime
import streamlit as st
import pandas as pd
import os
from dateutil.relativedelta import relativedelta

#Load the data to a dataframe
#filepath = os.path.join('Dataset','HousePrice.csv')
#df = pd.read_csv(filepath)  
filepath = os.path.join(os.path.dirname(__file__), 'Dataset', 'HousePrice.csv')
df = pd.read_csv(filepath)

#WebScraping Results from Property Listing website
st.title("House Price Prediction Dataset-from Quicker")

#st.dataframe(df.head(5))

# Filter Options
numberofbhk = st.sidebar.selectbox("Select NumberOfBHK:",['All'] + sorted(df['NumberOfBHK'].unique().tolist()))
transaction = st.sidebar.selectbox("Select Transaction:",['All'] + sorted(df['Transaction'].unique().tolist()))
availability = st.sidebar.selectbox("Select Availability:",['All'] + sorted(df['Availability'].unique().tolist()))
with st.sidebar:
    st.write("Posted Date Range Filter")
    col1, col2 = st.columns(2)

    with col1:
        startdate = st.date_input(
            "Start Date:",
            value=datetime.today() - relativedelta(months=2),
            label_visibility="collapsed" 
        )
        #st.caption("Start Date")

    with col2:
        enddate = st.date_input(
            "End Date:",
            value=datetime.today(),
            label_visibility="collapsed"  
        )
        #st.caption("End Date")

df['PostedDate'] = pd.to_datetime(df['PostedDate'], format='%d-%b-%Y')
postedby = st.sidebar.selectbox("Select Posted By:",['All']+ sorted(df['PostedBy'].unique().tolist()))
reraapproved = st.sidebar.selectbox("Select Rera Appproved:",['All']+ sorted(df['ReraApproved'].unique().tolist()))
areaname = st.sidebar.selectbox("Select Area Name:",['All']+sorted(df['AreaName'].unique().tolist()))
filtered_df = df[((df['PostedDate'].dt.date >= pd.to_datetime(startdate).date()) & (df['PostedDate'].dt.date <= pd.to_datetime(enddate).date())) 
                & ((df['NumberOfBHK'] == numberofbhk) if numberofbhk!='All' else True)
                & ((df['Transaction'] == transaction) if transaction!='All' else True)
                & ((df['Availability'] == availability) if availability!='All' else True)
                & ((df['PostedBy'] == postedby) if postedby!='All' else True)
                & ((df['ReraApproved'] == reraapproved) if reraapproved!='All' else True)
                & ((df['AreaName'] == areaname) if areaname!='All' else True)
                ]

filtered_df.reset_index(drop=True)
#st.write("Filtered Data:")
st.dataframe(filtered_df)
