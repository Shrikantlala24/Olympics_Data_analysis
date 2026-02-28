import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

import pre_process, helper
df = pre_process.pre()


# Sidebar Interface
# header
st.sidebar.header("Controls", text_alignment="center")

# dataset dekh le
main_frame = st.sidebar.checkbox('**Show the dataframe**')

# Analysis options
user = st.sidebar.radio(
    '**Select the analysis**',
    (
        'Medal-wise Analysis',
        'Country-wise Analysis',
        'Sport-wise Analysis',
        'Athlete-wise Analysis'
    )
)



# ----
# Functions to display the content based on user selection

# 
if main_frame:
    st.header("Summer Olympics Dataset")
    st.write("This dataset contains information about athletes, their participation in the Summer Olympics, and the medals they won.")
    st.dataframe(df)


if user == 'Medal-wise Analysis':
    st.header("Medal-wise Analysis")
    st.write("This section will provide insights into the distribution of medals across different countries and sports.")

    medal_tally = helper.medal(df)
    st.subheader("Medal Tally by Country")
    st.dataframe(medal_tally)

    # now based on dropbox selection
    st.sidebar.subheader("Select Country and Year for Trend")

    country = st.sidebar.selectbox("Country", helper.return_country_list(medal_tally), key='country_select', )
    year = st.sidebar.selectbox("Year",helper.return_year_list(df), key='year_select')

    # now let's call the functions we made for selection logic in helper.py
    medal_tally_filtered = helper.fetch_Medal_tally(country, year)
    st.subheader(f"Medal Tally for {country} in {year}")
    st.dataframe(medal_tally_filtered)



