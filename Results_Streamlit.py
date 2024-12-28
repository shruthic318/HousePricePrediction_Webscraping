from datetime import datetime
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

#filtered_df=filtered_df.copy().reset_index(drop=True)
filtered_df=filtered_df.iloc[:,1:]

st.dataframe(filtered_df)
