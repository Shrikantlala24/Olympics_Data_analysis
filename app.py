from time import time

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import streamlit as st

df = pd.read_csv("Data/athlete_events.csv")
st.dataframe(df)


st.sidebar.header("Controls", text_alignment="center")
st.sidebar.radio(
    'Select the analysis',
    (
        'Medal-wise Analysis',
        'Country-wise Analysis',
        'Sport-wise Analysis',
        'Athlete-wise Analysis'
    )
)

