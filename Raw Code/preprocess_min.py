
from matplotlib.pyplot import summer
import pandas as pd
import numpy as np

athletes = pd.read_csv("Data/athlete_events.csv")
regions = pd.read_csv("Data/noc_regions.csv")


def pre_process():

    global athletes, regions

# sirf summer nikal
    df = athletes[athletes['Season'] == "Summer"].copy()

# cleaning kar, but missing data ka kuch nhi abhi
    df.drop_duplicates(inplace=True)

# medal ki encoding kar + concat kar summer mein
    encod = pd.get_dummies(df.Medal).astype(int)
    summer = pd.concat([df, encod], axis=1)



    return summer