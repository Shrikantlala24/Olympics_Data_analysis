"""Olympics data preprocessing for Summer Olympics analysis."""

from pathlib import Path

import pandas as pd


def pre():
    """Load and preprocess Olympics data."""
    # Load datasets
    base_dir = Path(__file__).resolve().parent
    athletes_path = base_dir / "Data" / "athlete_events.csv"
    regions_path = base_dir / "Data" / "noc_regions.csv"

    usecols = [
        'Name', 'Sex', 'Age', 'Height', 'Weight', 'Team', 'NOC',
        'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal'
    ]
    dtypes = {
        'Year': 'int16',
        'Age': 'float32',
        'Height': 'float32',
        'Weight': 'float32',
        'Sex': 'category',
        'Season': 'category',
        'NOC': 'category',
        'Medal': 'category'
    }

    athletes = pd.read_csv(
        athletes_path,
        usecols=usecols,
        dtype=dtypes,
        low_memory=False
    )
    regions = pd.read_csv(
        regions_path,
        usecols=['NOC', 'region'],
        dtype={'NOC': 'category', 'region': 'string'},
        low_memory=False
    )
    regions.drop_duplicates(subset=['NOC'], inplace=True)
    
    # Filter Summer Olympics and remove duplicates
    summer = athletes[athletes['Season'] == "Summer"].drop_duplicates()

    # cleaning kar, but missing data ka kuch nhi abhi
    summer.drop_duplicates(inplace=True)

    
    # Merge with regions
    summer = summer.merge(regions, on="NOC", how="left")
    
    # Encode medals as binary columns
    medal_encoded = pd.get_dummies(summer['Medal'], dtype='int8')
    for medal in ['Gold', 'Silver', 'Bronze']:
        if medal not in medal_encoded.columns:
            medal_encoded[medal] = 0
    medal_encoded = medal_encoded[['Gold', 'Silver', 'Bronze']]
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
