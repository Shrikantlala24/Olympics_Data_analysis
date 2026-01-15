import pandas as pd
athlete = pd.read_csv('Data/athlete_events.csv')
regions = pd.read_csv('Data/noc_regions.csv')

def pre_process():
    global athlete, regions
    # here are the tasks we need to do in this project :-
    # preprocessing

    # todo 1. get only the summer olympics data
    # todo 2. merge the two datasets
    # todo 3. dropping the duplicate rows
    # todo 5. creating medal dataframe
    # todo 6. merging medal dataframe with summer dataframe

    athlete = athlete[athlete['Season'] == 'Summer']
    athlete = athlete.merge(regions, on='NOC', how='left')
    athlete.drop_duplicates(inplace=True)

    athlete = pd.concat([athlete, pd.get_dummies(athlete['Medal'])], axis=1)
    return athlete