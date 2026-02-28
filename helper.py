medal_tally = None
df = None
def medal(df_passed):
    global df, medal_tally
    df = df_passed
    # summer.Sport.value_counts()
    medal_counting = df.drop_duplicates(subset=['Team', 'NOC','Games','Year','Season','City','Sport', 'Event', 'Medal'])
    # Team	NOC	Games	Year	Season	City	Sport	Event
    medal_tally = medal_counting.groupby('region')[['Gold', 'Silver', 'Bronze']].sum().sort_values('Gold', ascending=False)

    # medal tally is df for medal tally of each country in each olympics

    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    return medal_tally

def return_country_list(medal_tally):
    country =  ['Overall'] + medal_tally.index.sort_values().tolist()


    return country

def return_year_list(df):
    year = ['Overall'] + sorted(df['Year'].unique().tolist())
    return year

def fetch_Medal_tally(country,year):
    if country == 'Overall' and year == 'Overall':
        return medal_tally
    elif country == 'Overall' and year != 'Overall':
        df_year = df[df['Year'] == year]
        return df_year
    elif country != 'Overall' and year == 'Overall':
        df_country = df[df['region'] == country]
        return df_country
    else:
        df_country_year = df[(df['region'] == country) & (df['Year'] == year)]
        return df_country_year
