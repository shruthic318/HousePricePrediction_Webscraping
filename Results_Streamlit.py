import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

#Load the data to a dataframe
filepath = os.path.join('Dataset','HousePrice.csv')
df = pd.read_csv(filepath)  

#WebScraping Results from Property Listing website
st.title("House Price Prediction Dataset-from Quicker")

st.dataframe(df.head(5))


