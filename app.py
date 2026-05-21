import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px

import pre_process, helper


@st.cache_data(show_spinner=False)
def load_data():
    return pre_process.pre()

@st.cache_data(show_spinner=False)
def load_medal_df(data):
    return helper.get_medal_df(data)

# setting page configuration
st.set_page_config(
    page_title="🏅 Olympics Data Analysis",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="expanded"
)

df = load_data()
medal_df = load_medal_df(df)
helper.medal(df)


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

if user == 'Medal Tally':
    st.header("Medal-wise Analysis")
    st.write(
        "This section will provide insights into the distribution of medals across different countries and their performance over time."
    )
    st.success(
        '🧩 This analysis allows you to filter the medal tally by country and year. Use the sidebar controls to select your desired country and year to see the corresponding medal tally.'
    )

    st.sidebar.subheader("Select Country and Year for Trend")
    countries = helper.get_country_list(df, include_overall=True)
    years = helper.get_year_list(df, include_overall=True)

    country = st.sidebar.selectbox("Country", countries, key='medal_country')
    year = st.sidebar.selectbox("Year", years, key='medal_year')

    medal_tally_filtered = helper.fetch_Medal_tally(country, year)
    st.subheader(f"Medal Tally for {country} in {year} years")

    st.sidebar.info('You can view either Dataframe or Table format.')
    view = st.sidebar.checkbox('View full Table', key='medal_table_view')

    medal_table = medal_tally_filtered.reset_index()
    if view:
        st.table(medal_table)
    else:
        st.dataframe(medal_table)

    st.divider()

    st.subheader("Top Countries by Medals")
    top_n = st.sidebar.slider("Top countries", 5, 30, 10, key='medal_top_n')
    top_countries = helper.top_countries_by_year(df, year, top_n=top_n, medal_df=medal_df)
    if top_countries.empty:
        st.info("No medal data available for this selection.")
    else:
        fig = px.bar(
            top_countries,
            x='region',
            y=['Gold', 'Silver', 'Bronze'],
            labels={'region': 'Country', 'value': 'Medals', 'variable': 'Medal'},
            title=f"Top {top_n} Countries by Medals ({year})"
        )
        fig.update_layout(barmode='stack')
        fig.update_xaxes(categoryorder='array', categoryarray=top_countries['region'])
        st.plotly_chart(fig, use_container_width=True)

    if country != 'Overall':
        st.subheader(f"{country} Medal Trend")
        country_trend = helper.country_medal_tally_by_year(df, country, medal_df=medal_df)
        if country_trend.empty:
            st.info("No medal trend data available for this country.")
        else:
            fig = px.line(
                country_trend,
                x='Year',
                y='Total',
                markers=True,
                labels={'Total': 'Medals'}
            )
            st.plotly_chart(fig, use_container_width=True)

            fig2 = px.area(
                country_trend,
                x='Year',
                y=['Gold', 'Silver', 'Bronze'],
                labels={'value': 'Medals', 'variable': 'Medal'}
            )
            st.plotly_chart(fig2, use_container_width=True)

        breakdown = helper.country_medal_breakdown(df, country, medal_df=medal_df)
        if not breakdown.empty:
            fig3 = px.pie(
                breakdown,
                values='Count',
                names='Medal',
                title=f"{country} Medal Breakdown"
            )
            st.plotly_chart(fig3, use_container_width=True)


if user == 'Overall Analysis':
    st.title("Overall Analysis")
    st.success("Here we'll show the key statistics of the data, as an overlook on the information")

    editions = df['Year'].nunique()
    cities = df['City'].nunique()
    sports = df['Sport'].nunique()
    events = df['Event'].nunique()
    athletes = df['Name'].nunique()
    nations = df['region'].nunique()
    total_medals = int(medal_df[['Gold', 'Silver', 'Bronze']].sum().sum())
    medal_events = int(medal_df.drop_duplicates(['Year', 'Event', 'Sport']).shape[0])
    teams = df['Team'].nunique()

    st.header("Key Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Editions", editions)
    with col2:
        st.metric("Host Cities", cities)
    with col3:
        st.metric("Sports", sports)

    col4, col5, col6 = st.columns(3)
    with col4:
        st.metric("Events", events)
    with col5:
        st.metric("Athletes", athletes)
    with col6:
        st.metric("Participating Nations", nations)

    col7, col8, col9 = st.columns(3)
    with col7:
        st.metric("Total Medals Awarded", total_medals)
    with col8:
        st.metric("Medal Events", medal_events)
    with col9:
        st.metric("Teams", teams)

    st.divider()

    st.header("Trends Over the Years")

    st.subheader("Participating Nations Over the Years")
    nations_per_year = helper.Nations_per_year(df)
    fig = px.line(nations_per_year, x='Year', y='nations', markers=True)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Participating Athletes Over the Years")
    athletes_per_year = helper.Athletes_per_year(df)
    fig2 = px.line(athletes_per_year, x='Year', y='athletes', markers=True)
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Sports Over the Years")
    sports_per_year = helper.Sports_per_year(df)
    fig3 = px.line(sports_per_year, x='Year', y='sports', markers=True)
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Events Over the Years")
    events_per_year = helper.Events_per_year(df)
    fig4 = px.line(events_per_year, x='Year', y='events', markers=True)
    st.plotly_chart(fig4, use_container_width=True)

    st.subheader("Medals Awarded Over the Years")
    medals_per_year = helper.Medals_per_year(df, medal_df=medal_df)
    fig5 = px.line(medals_per_year, x='Year', y='Total', markers=True)
    st.plotly_chart(fig5, use_container_width=True)

    st.subheader("Gender Participation Over the Years")
    gender_participation = helper.Gender_participation_over_years(df)
    fig6 = px.area(
        gender_participation,
        x='Year',
        y='athletes',
        color='Sex',
        labels={'athletes': 'Athletes'}
    )
    st.plotly_chart(fig6, use_container_width=True)

    st.divider()

    st.header("Top Performers")

    st.subheader("Top Countries by Total Medals")
    top_countries = helper.top_countries_overall(df, top_n=10, medal_df=medal_df)
    if not top_countries.empty:
        fig7 = px.bar(
            top_countries,
            x='Total',
            y='region',
            orientation='h',
            labels={'region': 'Country', 'Total': 'Total Medals'}
        )
        fig7.update_yaxes(categoryorder='array', categoryarray=top_countries['region'][::-1])
        st.plotly_chart(fig7, use_container_width=True)

    st.subheader("Top Sports by Total Medals")
    top_sports = helper.top_sports_overall(df, top_n=10, medal_df=medal_df)
    if not top_sports.empty:
        fig8 = px.bar(
            top_sports,
            x='Total',
            y='Sport',
            orientation='h',
            labels={'Sport': 'Sport', 'Total': 'Total Medals'}
        )
        fig8.update_yaxes(categoryorder='array', categoryarray=top_sports['Sport'][::-1])
        st.plotly_chart(fig8, use_container_width=True)

    st.header('No. of Events in Each Sport Over the Years')
    heatmap_data = helper.sport_event_heatmap(df)
    fig9, ax = plt.subplots(figsize=(16, 10))
    sns.heatmap(heatmap_data, cmap='YlGnBu', ax=ax)
    st.pyplot(fig9)


if user == 'Country-wise Analysis':
    st.header("Country-wise Analysis")
    st.write("Deep dive into medals, participation, and strengths for a selected country.")

    countries = helper.get_country_list(df)
    default_index = countries.index('India') if 'India' in countries else 0
    country = st.sidebar.selectbox(
        "Country",
        countries,
        index=default_index,
        key='country_analysis'
    )

    summary = helper.country_summary(df, country, medal_df=medal_df)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Medals", summary['total_medals'])
    with col2:
        st.metric("Gold", summary['gold'])
    with col3:
        st.metric("Silver", summary['silver'])
    with col4:
        st.metric("Bronze", summary['bronze'])

    col5, col6, col7, col8 = st.columns(4)
    with col5:
        st.metric("First Year", summary['first_year'] or "N/A")
    with col6:
        st.metric("Last Year", summary['last_year'] or "N/A")
    with col7:
        st.metric("Sports", summary['sports_count'])
    with col8:
        st.metric("Athletes", summary['athletes_count'])

    col9, col10 = st.columns(2)
    with col9:
        st.metric("Top Sport", summary['top_sport'] or "N/A")
    with col10:
        st.metric("Best Year", summary['best_year'] or "N/A")

    st.subheader("Medal Trend Over the Years")
    country_trend = helper.country_medal_tally_by_year(df, country, medal_df=medal_df)
    if country_trend.empty:
        st.info("No medal trend data available for this country.")
    else:
        fig = px.line(country_trend, x='Year', y='Total', markers=True)
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Medal Breakdown")
    breakdown = helper.country_medal_breakdown(df, country, medal_df=medal_df)
    if not breakdown.empty:
        fig2 = px.pie(breakdown, values='Count', names='Medal')
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Top Sports for the Country")
    top_sports = helper.country_top_sports(df, country, top_n=10, medal_df=medal_df)
    if not top_sports.empty:
        fig3 = px.bar(
            top_sports,
            x='Total',
            y='Sport',
            orientation='h',
            labels={'Total': 'Total Medals'}
        )
        fig3.update_yaxes(categoryorder='array', categoryarray=top_sports['Sport'][::-1])
        st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Top Athletes for the Country")
    top_athletes = helper.country_top_athletes(df, country, top_n=10)
    if not top_athletes.empty:
        fig4 = px.bar(
            top_athletes,
            x='Medals',
            y='Name',
            orientation='h',
            labels={'Medals': 'Medals'}
        )
        fig4.update_yaxes(categoryorder='array', categoryarray=top_athletes['Name'][::-1])
        st.plotly_chart(fig4, use_container_width=True)

    st.subheader("Gender Participation Over the Years")
    country_gender = helper.country_gender_participation(df, country)
    if not country_gender.empty:
        fig5 = px.area(
            country_gender,
            x='Year',
            y='athletes',
            color='Sex',
            labels={'athletes': 'Athletes'}
        )
        st.plotly_chart(fig5, use_container_width=True)

    st.subheader("Medals by Sport Over the Years")
    heatmap = helper.country_sport_medal_heatmap(df, country, medal_df=medal_df)
    if not heatmap.empty:
        fig6, ax = plt.subplots(figsize=(16, 10))
        sns.heatmap(heatmap, cmap='YlGnBu', ax=ax)
        st.pyplot(fig6)


if user == 'Sport-wise Analysis':
    st.header("Sport-wise Analysis")
    st.write("Explore medal trends, top countries, and athlete highlights for a selected sport.")

    sport = st.sidebar.selectbox(
        "Sport",
        helper.get_sport_list(df),
        key='sport_analysis'
    )

    summary = helper.sport_summary(df, sport, medal_df=medal_df)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Medals", summary['total_medals'])
    with col2:
        st.metric("Gold", summary['gold'])
    with col3:
        st.metric("Silver", summary['silver'])
    with col4:
        st.metric("Bronze", summary['bronze'])

    col5, col6, col7, col8 = st.columns(4)
    with col5:
        st.metric("Total Events", summary['total_events'])
    with col6:
        st.metric("First Year", summary['first_year'] or "N/A")
    with col7:
        st.metric("Last Year", summary['last_year'] or "N/A")
    with col8:
        st.metric("Top Country", summary['top_country'] or "N/A")

    st.subheader("Event Trend Over the Years")
    event_trend = helper.sport_event_trend(df, sport)
    if not event_trend.empty:
        fig = px.line(event_trend, x='Year', y='events', markers=True)
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Medal Trend Over the Years")
    medal_trend = helper.sport_medal_trend(df, sport, medal_df=medal_df)
    if not medal_trend.empty:
        fig2 = px.line(medal_trend, x='Year', y='Total', markers=True)
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Medal Breakdown")
    breakdown = helper.sport_medal_breakdown(df, sport, medal_df=medal_df)
    if not breakdown.empty:
        fig3 = px.pie(breakdown, values='Count', names='Medal')
        st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Top Countries in this Sport")
    top_countries = helper.sport_top_countries(df, sport, top_n=10, medal_df=medal_df)
    if not top_countries.empty:
        fig4 = px.bar(
            top_countries,
            x='Total',
            y='region',
            orientation='h',
            labels={'region': 'Country', 'Total': 'Total Medals'}
        )
        fig4.update_yaxes(categoryorder='array', categoryarray=top_countries['region'][::-1])
        st.plotly_chart(fig4, use_container_width=True)

    st.subheader("Top Athletes in this Sport")
    top_athletes = helper.sport_top_athletes(df, sport, top_n=10)
    if not top_athletes.empty:
        fig5 = px.bar(
            top_athletes,
            x='Medals',
            y='Name',
            orientation='h',
            labels={'Medals': 'Medals'}
        )
        fig5.update_yaxes(categoryorder='array', categoryarray=top_athletes['Name'][::-1])
        st.plotly_chart(fig5, use_container_width=True)

    st.subheader("Gender Participation Over the Years")
    gender = helper.sport_gender_participation(df, sport)
    if not gender.empty:
        fig6 = px.area(gender, x='Year', y='athletes', color='Sex', labels={'athletes': 'Athletes'})
        st.plotly_chart(fig6, use_container_width=True)

    st.subheader("Age Distribution of Medalists")
    age_data = helper.sport_age_distribution(df, sport)
    if not age_data.empty:
        fig7 = px.histogram(age_data, x='Age', color='Medal', nbins=30)
        st.plotly_chart(fig7, use_container_width=True)


if user == 'Athlete-wise Analysis':
    st.header("Athlete-wise Analysis")
    st.write("Explore medal leaders, participation patterns, and athlete profiles.")

    st.sidebar.subheader("Athlete Filters")
    sport_filter = st.sidebar.selectbox(
        "Sport",
        ['All'] + helper.get_sport_list(df),
        key='athlete_sport_filter'
    )
    gender_filter = st.sidebar.radio(
        "Gender",
        ['All', 'M', 'F'],
        key='athlete_gender_filter'
    )
    top_n = st.sidebar.slider("Top athletes", 5, 30, 15, key='athlete_top_n')

    st.subheader("Top Medalists")
    top_athletes = helper.top_athletes_overall(
        df,
        top_n=top_n,
        sport=sport_filter,
        gender=gender_filter
    )
    if not top_athletes.empty:
        fig = px.bar(
            top_athletes,
            x='Medals',
            y='Name',
            orientation='h',
            labels={'Medals': 'Medals'}
        )
        fig.update_yaxes(categoryorder='array', categoryarray=top_athletes['Name'][::-1])
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Most Participated Athletes")
    participations = helper.most_participated_athletes(
        df,
        top_n=top_n,
        sport=sport_filter,
        gender=gender_filter
    )
    if not participations.empty:
        fig2 = px.bar(
            participations,
            x='Games',
            y='Name',
            orientation='h',
            labels={'Games': 'Games'}
        )
        fig2.update_yaxes(categoryorder='array', categoryarray=participations['Name'][::-1])
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Age Distribution by Medal Type")
    age_data = helper.age_distribution_by_medal(
        df,
        sport=sport_filter,
        gender=gender_filter
    )
    if not age_data.empty:
        fig3 = px.histogram(
            age_data,
            x='Age',
            color='Medal',
            nbins=30,
            barmode='overlay'
        )
        st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Height vs Weight of Medalists")
    hw_data = helper.height_weight_medalists(
        df,
        sample_n=5000,
        sport=sport_filter,
        gender=gender_filter
    )
    if not hw_data.empty:
        fig4 = px.scatter(
            hw_data,
            x='Weight',
            y='Height',
            color='Medal',
            opacity=0.6
        )
        st.plotly_chart(fig4, use_container_width=True)

    st.sidebar.subheader("Athlete Spotlight")
    athlete_name = st.sidebar.text_input("Athlete name (exact)", key='athlete_name')
    if athlete_name:
        if (df['Name'] == athlete_name).any():
            profile = helper.athlete_profile(df, athlete_name)

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Medals", profile['total_medals'])
            with col2:
                st.metric("Gold", profile['gold'])
            with col3:
                st.metric("Silver", profile['silver'])
            with col4:
                st.metric("Bronze", profile['bronze'])

            col5, col6, col7, col8 = st.columns(4)
            with col5:
                st.metric("First Year", profile['first_year'] or "N/A")
            with col6:
                st.metric("Last Year", profile['last_year'] or "N/A")
            with col7:
                st.metric("Events", profile['events'])
            with col8:
                st.metric("Countries", ", ".join(profile['regions']) if profile['regions'] else "N/A")

            st.subheader("Medal Trend")
            medal_trend = helper.athlete_medal_trend(df, athlete_name)
            if not medal_trend.empty:
                fig5 = px.line(medal_trend, x='Year', y='Total', markers=True)
                st.plotly_chart(fig5, use_container_width=True)

            st.subheader("Medal Details")
            medal_table = helper.athlete_medal_table(df, athlete_name)
            if not medal_table.empty:
                st.dataframe(medal_table)
        else:
            st.warning("No athlete found with that exact name.")