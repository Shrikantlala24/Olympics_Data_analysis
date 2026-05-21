medal_tally = None
df = None
# Medal-wise analysis functions
def medal(df_passed, medal_df=None):
    global df, medal_tally, df2
    df = df_passed

    # summer.Sport.value_counts()
    if medal_df is None:
        df2 = df.drop_duplicates(subset=['Team', 'NOC','Games','Year','Season','City','Sport', 'Event', 'Medal'])
    else:
        df2 = medal_df
    # Team	NOC	Games	Year	Season	City	Sport	Event
    medal_tally = df2.groupby('region')[['Gold', 'Silver', 'Bronze']].sum().sort_values('Gold', ascending=False)

    # medal tally is df for medal tally of each country in each olympics
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    return medal_tally

def return_country_list(df_passed=None):
    if df_passed is None:
        if medal_tally is None and df is not None:
            medal(df)
        if medal_tally is None:
            return ['Overall']
        countries = medal_tally.index.sort_values().tolist()
    else:
        countries = sorted(df_passed['region'].dropna().unique().tolist())
    return ['Overall'] + countries

def return_year_list(df_passed=None):
    data = df if df_passed is None else df_passed
    if data is None:
        return ['Overall']
    years = sorted(data['Year'].dropna().unique().tolist())
    return ['Overall'] + years

def fetch_Medal_tally(country,year):

    if country == 'Overall' and year == 'Overall':
        return medal_tally
    
    elif country == 'Overall' and year != 'Overall':
        df_year = df2[df2['Year'] == year]
        medal_tally_year = df_year.groupby('region')[['Gold', 'Silver', 'Bronze']].sum().sort_values('Gold', ascending=False)
        x = medal_tally_year
    
    elif country != 'Overall' and year == 'Overall':
        df_country = df2[df2['region'] == country]

        medal_tally_country = df_country.groupby('Year')[['Gold', 'Silver', 'Bronze']].sum().sort_values('Year', ascending=True)
        # medal_tally_country = df_country.groupby('region')[['Gold', 'Silver', 'Bronze']].sum().sort_values('Gold', ascending=False)
        x = medal_tally_country
    
    else:
        df_country_year = df2[(df2['region'] == country) & (df2['Year'] == year)]
        medal_tally_country_year = df_country_year.groupby('region')[['Gold', 'Silver', 'Bronze']].sum().sort_values('Gold', ascending=False)
        x = medal_tally_country_year
    
    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']
    return x

# Overall analysis functions
def Nations_per_year(df):
    nations_per_year = (
        df.drop_duplicates(['Year', 'region'])
        .groupby('Year')
        .size()
        .reset_index(name='nations')
    )
    return nations_per_year

def Athletes_per_year(df):
    athletes_per_year = (
        df.drop_duplicates(['Year', 'Name'])
        .groupby('Year')
        .size()
        .reset_index(name='athletes')
    )
    return athletes_per_year

def Events_per_year(df):
    events_per_year = (
        df.drop_duplicates(['Year', 'Event'])
        .groupby('Year')
        .size()
        .reset_index(name='events')
    )
    return events_per_year

def Sports_per_year(df):
    sports_per_year = (
        df.drop_duplicates(['Year', 'Sport'])
        .groupby('Year')
        .size()
        .reset_index(name='sports')
    )
    return sports_per_year

def get_medal_df(df):
    return df.dropna(subset=['Medal']).drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal']
    )

def get_country_list(df, include_overall=False):
    countries = sorted(df['region'].dropna().unique().tolist())
    return ['Overall'] + countries if include_overall else countries

def get_year_list(df, include_overall=False):
    years = sorted(df['Year'].dropna().unique().tolist())
    return ['Overall'] + years if include_overall else years

def get_sport_list(df):
    return sorted(df['Sport'].dropna().unique().tolist())

def get_athlete_list(df):
    return sorted(df['Name'].dropna().unique().tolist())

def Medals_per_year(df, medal_df=None):
    medal_df = get_medal_df(df) if medal_df is None else medal_df
    medals_per_year = medal_df.groupby('Year')[['Gold', 'Silver', 'Bronze']].sum().reset_index()
    medals_per_year['Total'] = (
        medals_per_year['Gold'] + medals_per_year['Silver'] + medals_per_year['Bronze']
    )
    return medals_per_year

def Gender_participation_over_years(df):
    participation = df.drop_duplicates(['Year', 'Name', 'Sex'])
    gender = participation.groupby(['Year', 'Sex']).size().reset_index(name='athletes')
    return gender

def top_countries_overall(df, top_n=10, medal_df=None):
    medal_df = get_medal_df(df) if medal_df is None else medal_df
    data = medal_df.dropna(subset=['region'])
    tally = data.groupby('region')[['Gold', 'Silver', 'Bronze']].sum()
    tally['Total'] = tally['Gold'] + tally['Silver'] + tally['Bronze']
    return tally.sort_values('Total', ascending=False).head(top_n).reset_index()

def top_countries_by_year(df, year, top_n=10, medal_df=None):
    medal_df = get_medal_df(df) if medal_df is None else medal_df
    data = medal_df.dropna(subset=['region'])
    if year != 'Overall':
        data = data[data['Year'] == year]
    tally = data.groupby('region')[['Gold', 'Silver', 'Bronze']].sum()
    tally['Total'] = tally['Gold'] + tally['Silver'] + tally['Bronze']
    return tally.sort_values('Total', ascending=False).head(top_n).reset_index()

def top_sports_overall(df, top_n=10, medal_df=None):
    medal_df = get_medal_df(df) if medal_df is None else medal_df
    tally = medal_df.groupby('Sport')[['Gold', 'Silver', 'Bronze']].sum()
    tally['Total'] = tally['Gold'] + tally['Silver'] + tally['Bronze']
    return tally.sort_values('Total', ascending=False).head(top_n).reset_index()

def sport_event_heatmap(df):
    data = df.drop_duplicates(['Event', 'Sport', 'Year'])
    heatmap = (
        data.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count')
        .fillna(0)
        .astype(int)
    )
    return heatmap

def country_summary(df, country, medal_df=None):
    medal_df = get_medal_df(df) if medal_df is None else medal_df
    country_rows = df[df['region'] == country]
    country_medals = medal_df[medal_df['region'] == country]
    medals_sum = country_medals[['Gold', 'Silver', 'Bronze']].sum()
    total_medals = int(medals_sum.sum()) if not country_medals.empty else 0
    first_year = int(country_rows['Year'].min()) if not country_rows.empty else None
    last_year = int(country_rows['Year'].max()) if not country_rows.empty else None
    sports_count = int(country_rows['Sport'].nunique()) if not country_rows.empty else 0
    athletes_count = int(country_rows['Name'].nunique()) if not country_rows.empty else 0
    top_sport = None
    best_year = None
    if not country_medals.empty:
        sport_tally = country_medals.groupby('Sport')[['Gold', 'Silver', 'Bronze']].sum()
        sport_tally['Total'] = sport_tally['Gold'] + sport_tally['Silver'] + sport_tally['Bronze']
        top_sport = sport_tally.sort_values('Total', ascending=False).index[0]
        year_tally = country_medals.groupby('Year')[['Gold', 'Silver', 'Bronze']].sum()
        year_tally['Total'] = year_tally['Gold'] + year_tally['Silver'] + year_tally['Bronze']
        best_year = int(year_tally['Total'].idxmax())
    return {
        'total_medals': total_medals,
        'gold': int(medals_sum.get('Gold', 0)),
        'silver': int(medals_sum.get('Silver', 0)),
        'bronze': int(medals_sum.get('Bronze', 0)),
        'first_year': first_year,
        'last_year': last_year,
        'sports_count': sports_count,
        'athletes_count': athletes_count,
        'top_sport': top_sport,
        'best_year': best_year,
    }

def country_medal_tally_by_year(df, country, medal_df=None):
    medal_df = get_medal_df(df) if medal_df is None else medal_df
    data = medal_df[medal_df['region'] == country]
    tally = data.groupby('Year')[['Gold', 'Silver', 'Bronze']].sum().reset_index()
    tally['Total'] = tally['Gold'] + tally['Silver'] + tally['Bronze']
    return tally

def country_medal_breakdown(df, country, medal_df=None):
    medal_df = get_medal_df(df) if medal_df is None else medal_df
    data = medal_df[medal_df['region'] == country]
    medals_sum = data[['Gold', 'Silver', 'Bronze']].sum()
    breakdown = medals_sum.reset_index()
    breakdown.columns = ['Medal', 'Count']
    return breakdown

def country_top_sports(df, country, top_n=10, medal_df=None):
    medal_df = get_medal_df(df) if medal_df is None else medal_df
    data = medal_df[medal_df['region'] == country]
    tally = data.groupby('Sport')[['Gold', 'Silver', 'Bronze']].sum()
    tally['Total'] = tally['Gold'] + tally['Silver'] + tally['Bronze']
    return tally.sort_values('Total', ascending=False).head(top_n).reset_index()

def country_top_athletes(df, country, top_n=10):
    data = df[(df['region'] == country) & (df['Medal'].notna())]
    tally = data.groupby('Name').size().sort_values(ascending=False).head(top_n).reset_index(name='Medals')
    return tally

def country_sport_medal_heatmap(df, country, medal_df=None):
    medal_df = get_medal_df(df) if medal_df is None else medal_df
    data = medal_df[medal_df['region'] == country]
    heatmap = (
        data.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count')
        .fillna(0)
        .astype(int)
    )
    return heatmap

def country_gender_participation(df, country):
    data = df[df['region'] == country].drop_duplicates(['Year', 'Name', 'Sex'])
    gender = data.groupby(['Year', 'Sex']).size().reset_index(name='athletes')
    return gender

def sport_summary(df, sport, medal_df=None):
    medal_df = get_medal_df(df) if medal_df is None else medal_df
    sport_rows = df[df['Sport'] == sport]
    sport_medals = medal_df[medal_df['Sport'] == sport]
    medals_sum = sport_medals[['Gold', 'Silver', 'Bronze']].sum()
    total_medals = int(medals_sum.sum()) if not sport_medals.empty else 0
    total_events = int(sport_rows['Event'].nunique()) if not sport_rows.empty else 0
    first_year = int(sport_rows['Year'].min()) if not sport_rows.empty else None
    last_year = int(sport_rows['Year'].max()) if not sport_rows.empty else None
    top_country = None
    top_athlete = None
    if not sport_medals.empty:
        country_tally = sport_medals.groupby('region')[['Gold', 'Silver', 'Bronze']].sum()
        country_tally['Total'] = country_tally['Gold'] + country_tally['Silver'] + country_tally['Bronze']
        top_country = country_tally.sort_values('Total', ascending=False).index[0]
    medalists = sport_rows[sport_rows['Medal'].notna()]
    if not medalists.empty:
        top_athlete = medalists.groupby('Name').size().sort_values(ascending=False).index[0]
    return {
        'total_medals': total_medals,
        'gold': int(medals_sum.get('Gold', 0)),
        'silver': int(medals_sum.get('Silver', 0)),
        'bronze': int(medals_sum.get('Bronze', 0)),
        'total_events': total_events,
        'first_year': first_year,
        'last_year': last_year,
        'top_country': top_country,
        'top_athlete': top_athlete,
    }

def sport_medal_trend(df, sport, medal_df=None):
    medal_df = get_medal_df(df) if medal_df is None else medal_df
    data = medal_df[medal_df['Sport'] == sport]
    tally = data.groupby('Year')[['Gold', 'Silver', 'Bronze']].sum().reset_index()
    tally['Total'] = tally['Gold'] + tally['Silver'] + tally['Bronze']
    return tally

def sport_event_trend(df, sport):
    data = df[df['Sport'] == sport].drop_duplicates(['Year', 'Event'])
    events = data.groupby('Year').size().reset_index(name='events')
    return events

def sport_medal_breakdown(df, sport, medal_df=None):
    medal_df = get_medal_df(df) if medal_df is None else medal_df
    data = medal_df[medal_df['Sport'] == sport]
    medals_sum = data[['Gold', 'Silver', 'Bronze']].sum()
    breakdown = medals_sum.reset_index()
    breakdown.columns = ['Medal', 'Count']
    return breakdown

def sport_top_countries(df, sport, top_n=10, medal_df=None):
    medal_df = get_medal_df(df) if medal_df is None else medal_df
    data = medal_df[medal_df['Sport'] == sport].dropna(subset=['region'])
    tally = data.groupby('region')[['Gold', 'Silver', 'Bronze']].sum()
    tally['Total'] = tally['Gold'] + tally['Silver'] + tally['Bronze']
    return tally.sort_values('Total', ascending=False).head(top_n).reset_index()

def sport_top_athletes(df, sport, top_n=10):
    data = df[(df['Sport'] == sport) & (df['Medal'].notna())]
    tally = data.groupby('Name').size().sort_values(ascending=False).head(top_n).reset_index(name='Medals')
    return tally

def sport_gender_participation(df, sport):
    data = df[df['Sport'] == sport].drop_duplicates(['Year', 'Name', 'Sex'])
    gender = data.groupby(['Year', 'Sex']).size().reset_index(name='athletes')
    return gender

def sport_age_distribution(df, sport):
    data = df[(df['Sport'] == sport) & (df['Medal'].notna())][['Age', 'Medal']]
    return data.dropna(subset=['Age'])

def top_athletes_overall(df, top_n=10, sport=None, gender=None):
    data = df[df['Medal'].notna()].copy()
    if sport and sport != 'All':
        data = data[data['Sport'] == sport]
    if gender and gender != 'All':
        data = data[data['Sex'] == gender]
    tally = data.groupby('Name').size().sort_values(ascending=False).head(top_n).reset_index(name='Medals')
    return tally

def most_participated_athletes(df, top_n=10, sport=None, gender=None):
    data = df.copy()
    if sport and sport != 'All':
        data = data[data['Sport'] == sport]
    if gender and gender != 'All':
        data = data[data['Sex'] == gender]
    participations = (
        data.drop_duplicates(['Name', 'Games'])
        .groupby('Name')
        .size()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index(name='Games')
    )
    return participations

def age_distribution_by_medal(df, sport=None, gender=None):
    data = df[df['Medal'].notna()]
    if sport and sport != 'All':
        data = data[data['Sport'] == sport]
    if gender and gender != 'All':
        data = data[data['Sex'] == gender]
    return data[['Age', 'Medal']].dropna(subset=['Age'])

def height_weight_medalists(df, sample_n=5000, random_state=42, sport=None, gender=None):
    data = df[df['Medal'].notna()]
    if sport and sport != 'All':
        data = data[data['Sport'] == sport]
    if gender and gender != 'All':
        data = data[data['Sex'] == gender]
    data = data[['Height', 'Weight', 'Medal']].dropna()
    if len(data) > sample_n:
        data = data.sample(sample_n, random_state=random_state)
    return data

def athlete_profile(df, athlete_name):
    data = df[df['Name'] == athlete_name]
    medal_rows = data[data['Medal'].notna()]
    medals_sum = medal_rows[['Gold', 'Silver', 'Bronze']].sum()
    total_medals = int(medals_sum.sum()) if not medal_rows.empty else 0
    sports = sorted(data['Sport'].dropna().unique().tolist())
    regions = sorted(data['region'].dropna().unique().tolist())
    first_year = int(data['Year'].min()) if not data.empty else None
    last_year = int(data['Year'].max()) if not data.empty else None
    return {
        'total_medals': total_medals,
        'gold': int(medals_sum.get('Gold', 0)),
        'silver': int(medals_sum.get('Silver', 0)),
        'bronze': int(medals_sum.get('Bronze', 0)),
        'sports': sports,
        'regions': regions,
        'first_year': first_year,
        'last_year': last_year,
        'events': int(data['Event'].nunique()) if not data.empty else 0,
    }

def athlete_medal_trend(df, athlete_name):
    data = df[(df['Name'] == athlete_name) & (df['Medal'].notna())]
    tally = data.groupby('Year')[['Gold', 'Silver', 'Bronze']].sum().reset_index()
    tally['Total'] = tally['Gold'] + tally['Silver'] + tally['Bronze']
    return tally

def athlete_medal_table(df, athlete_name):
    data = df[(df['Name'] == athlete_name) & (df['Medal'].notna())]
    return data[['Year', 'City', 'Sport', 'Event', 'Medal', 'Team']].sort_values('Year')
