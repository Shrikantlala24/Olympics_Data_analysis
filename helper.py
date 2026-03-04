medal_tally = None
df = None
# Medal-wise analysis functions
def medal(df_passed):
    global df, medal_tally, df2
    df = df_passed

    # summer.Sport.value_counts()
    df2 = df.drop_duplicates(subset=['Team', 'NOC','Games','Year','Season','City','Sport', 'Event', 'Medal'])
    # Team	NOC	Games	Year	Season	City	Sport	Event
    medal_tally = df2.groupby('region')[['Gold', 'Silver', 'Bronze']].sum().sort_values('Gold', ascending=False)

    # medal tally is df for medal tally of each country in each olympics
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    return medal_tally

def return_country_list():
    country =  ['Overall'] + medal_tally.index.sort_values().tolist()
    return country

def return_year_list():
    year = ['Overall'] + sorted(df['Year'].unique().tolist())
    return year

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
    
    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']
    return x

# Overall analysis functions
def Nations_per_year(df):
    nations_per_year = df.drop_duplicates(['Year', 'region'])['Year'].value_counts().sort_index().reset_index()
    nations_per_year.rename(columns={ 'nations': 'Year', 'count': 'nations' }, inplace=True)
    return nations_per_year

def Athletes_per_year(df):
    athletes_per_year = df.drop_duplicates(['Year', 'Name'])['Year'].value_counts().sort_index().reset_index()
    athletes_per_year.rename(columns={ 'athletes': 'Year', 'count': 'athletes' }, inplace=True)
    return athletes_per_year

