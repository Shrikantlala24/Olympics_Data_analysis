import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px

import pre_process, helper


@st.cache_data(show_spinner=False)
def load_data():
    return pre_process.pre()


df = load_data()

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
        'Medal Tally',
        'Overall Analysis',
        'Country-wise Analysis',
        'Sport-wise Analysis',
        'Athlete-wise Analysis'
    )
)



# ----
# Functions to display the content based on user selection

# todo if og dataset show karna hai tohhh..
if main_frame:
    st.header("Summer Olympics Dataset")
    st.write("This dataset contains information about athletes, their participation in the Summer Olympics, and the medals they won.")
    st.dataframe(df)

# todo medal tally ka code
if user == 'Medal Tally':
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
    st.title("Overall Analysis")
    st.success("here we'll show the key statistics of the data, as a overlook on the information")
    

    editions = df['Year'].unique()
    Cities = df['City'].unique()
    sports = df['Sport'].unique()
    events = df['Event'].unique()
    athletes = df['Name'].unique()
    nations = df['region'].unique()

    # here we'll show the key statistics of the data, as information overlook
    st.header("Key Statistics")
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

    st.divider()

    #?  HERE in trends over the year section, WE HAVE CODE IN THIS WAY
    # 1. SUBHEADER
    # 2. fucntion call to take the desired df
    # 3. plotly code to show the line graph
    # 4. st.plotly_chart to show the graph

    st.header("Trends Over the Years")



    st.subheader("Participating Nations Over the Years")
    nations_per_year = helper.Nations_per_year(df)
    fig = px.line(nations_per_year, x='Year', y='nations')
    st.plotly_chart(fig)


    st.subheader("Participating Athletes Over the Years")
    athletes_per_year = helper.Athletes_per_year(df)
    fig2 = px.line(athletes_per_year, x='Year', y='athletes')
    st.plotly_chart(fig2)


    st.subheader("Events Over the Years")
    events_per_year = helper.Events_per_year(df)
    fig3 = px.line(events_per_year, x='Year', y='events')
    st.plotly_chart(fig3)

    # let's try heatmaps
    st.header('No. of Events in Each Sport Over the Years')
    
    x = df.drop_duplicates(['Event','Sport','Year'])
    x_pv = x.pivot_table(index = 'Sport', columns= 'Year', values='Event', aggfunc='count').fillna(0).astype(int)
    
    plt.figure(figsize=(20, 20))
    sns.heatmap(x_pv, annot=True, fmt="d")

    st.pyplot(plt)