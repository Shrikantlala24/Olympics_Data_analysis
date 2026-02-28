def medal(df):
    # summer.Sport.value_counts()
    medal_counting = df.drop_duplicates(subset=['Team', 'NOC','Games','Year','Season','City','Sport', 'Event', 'Medal'])
    # Team	NOC	Games	Year	Season	City	Sport	Event
    medal_tally = medal_counting.groupby('region')[['Gold', 'Silver', 'Bronze']].sum().sort_values('Gold', ascending=False)

    # medal tally is df for medal tally of each country in each olympics

    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    return medal_tally

def return_list(medal_tally):
    country = medal_tally.index.tolist()
    return country