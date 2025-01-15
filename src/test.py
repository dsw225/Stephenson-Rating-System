import pyreadr
import pandas as pd
import numpy as np
import datetime
import time
import copy
from stephenson import *

result = pyreadr.read_r('../data/aflodds.rda')
r_df = list(result.values())[0]
df = pd.DataFrame(r_df)
df.head()

week_one = df[(df['Week'] == 1.0)]

combined_teams = pd.concat([week_one['HomeTeam'], week_one['AwayTeam']]) 
all_teams = combined_teams.drop_duplicates().tolist()

team_data = {
    'team': all_teams,   
    'steph_rating': [Stephenson() for _ in all_teams],
}
df = pd.DataFrame(team_data)
df.head()

for index, row in week_one.iterrows():
    home_rating = df.loc[df['team'] == row['HomeTeam'], 'steph_rating'].values[0]
    away_rating = df.loc[df['team'] == row['AwayTeam'], 'steph_rating'].values[0]

    # Since this is only week one ignore as its first week
    # home_rating.updateVar(i['Date'])
    # away_rating.updateVar(i['Date'])

    # So we don't evaluate on outcome
    home_clone = copy.deepcopy(home_rating)

    home_rating.newVarRating(away_rating, row['Score'], 1) #pone is 1 for home team - since default gamma is 0 this is irrelevant
    away_rating.newVarRating(home_clone, (1 - row['Score']), 0) 

    df.loc[df['team'] == row['HomeTeam'], 'steph_rating'] = home_rating
    df.loc[df['team'] == row['AwayTeam'], 'steph_rating'] = away_rating

for index, row in df.iterrows():
    print(f"{row['team']}:", end=" ")
    row['steph_rating'].printVals()