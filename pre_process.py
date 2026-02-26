"""Olympics data preprocessing for Summer Olympics analysis."""

import pandas as pd


def pre():
    """Load and preprocess Olympics data."""
    # Load datasets
    athletes = pd.read_csv("Data/athlete_events.csv")
    regions = pd.read_csv("Data/noc_regions.csv")
    
    # Filter Summer Olympics and remove duplicates
    summer = athletes[athletes['Season'] == "Summer"].drop_duplicates()

    # cleaning kar, but missing data ka kuch nhi abhi
    summer.drop_duplicates(inplace=True)

    
    # Merge with regions
    summer = summer.merge(regions, on="NOC", how="left")
    
    # Encode medals as binary columns
    medal_encoded = pd.get_dummies(summer['Medal']).astype(int)
    summer = pd.concat([summer, medal_encoded], axis=1)
    
    # # Calculate medal tally (one medal per event, not per athlete)
    # medal_tally = (
    #     summer.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    #     .groupby('NOC')[['Gold', 'Silver', 'Bronze']]
    #     .sum()
    #     .sort_values('Gold', ascending=False)
    # )
    
    return summer


if __name__ == "__main__":
    summer_df = pre()
    print("Summer Olympics DataFrame shape:", summer_df.shape)
