import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px

import pre_process, helper
df = pre_process.pre()

# setting page configuration
st.set_page_config(
    page_title="🏅 Olympics Data Analysis",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="expanded"
)


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
        'Overall Analysis',
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

# todo medal wise ka code
if user == 'Medal-wise Analysis':
    # pura interface medal wise analysis ke liye

    st.header("Medal-wise Analysis")
    st.write("This section will provide insights into the distribution of medals across different countries and their performance over time.")
    st.success('🧩 This analysis allows you to filter the medal tally by country and year. Use the sidebar controls to select your desired country and year to see the corresponding medal tally.')

    # medal tally wali table fetch karle and code ke context mein le ayyen
    # because pura code is medal tally
    medal_tally = helper.medal(df)

    # now based on dropbox selection
    st.sidebar.subheader("Select Country and Year for Trend")


    country = st.sidebar.selectbox("Country", helper.return_country_list(), key='country_select', )
    year = st.sidebar.selectbox("Year",helper.return_year_list(), key='year_select')


    # now let's call the functions we made for selection logic in helper.py
    medal_tally_filtered = helper.fetch_Medal_tally(country, year)
    st.subheader(f"Medal Tally for {country} in {year} years")

    # table view ka logic
    st.sidebar.info('You can view either Dataframe or Table format.')
    view = st.sidebar.checkbox('View full Table')

    if view:
        st.table(medal_tally_filtered)
    else :
        st.dataframe(medal_tally_filtered)


# todo Overall analysis ka code
if user == 'Overall Analysis':
    st.header("Overall Analysis")
    st.success("This section will provide insights into the overall trends and patterns in the Summer Olympics dataset, including the number of editions, cities, sports/events, athletes, and participating nations.")
    

    editions = df['Year'].unique()
    Cities = df['City'].unique()
    sports = df['Sport'].unique()
    events = df['Event'].unique()
    athletes = df['Name'].unique()
    nations = df['region'].unique()

    st.subheader("Key Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Editions", len(editions))
    with col2:
        st.metric("Host Cities", len(Cities))
    with col3:
        st.metric("Sports", len(sports))
    

    col4, col5, col6 = st.columns(3)
    with col4:
        st.metric("Events", len(events))
    with col5:
        st.metric("Athletes", len(athletes))
    with col6:
        st.metric("Participating Nations", len(nations))

    nations_per_year = helper.Nations_per_year(df)
    # fig = px.line(nations_per_year, x='Year', y='nations', title='Number of Participating Nations Over the Years')
    # fig.show()
    st.line_chart(nations_per_year, x='Year', y='nations',)
