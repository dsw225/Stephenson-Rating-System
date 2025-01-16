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

weeks = df[(df['Week'] <= 12.0)]

combined_teams = pd.concat([weeks['HomeTeam'], weeks['AwayTeam']]) 
all_teams = combined_teams.drop_duplicates().tolist()

team_data = {
    'team': all_teams,   
    'steph_rating': [Stephenson() for _ in all_teams],
}
df_team = pd.DataFrame(team_data)
df_team.head()

for week, week_df in weeks.groupby('Week'):
    # print(f"Week {week}")
    for index, row in week_df.iterrows():
        home_rating = df_team.loc[df_team['team'] == row['HomeTeam'], 'steph_rating'].values[0]
        away_rating = df_team.loc[df_team['team'] == row['AwayTeam'], 'steph_rating'].values[0]

        #Replacing updateVal since this is not by date but by week 10^2 = 100 (cval)
        home_rating.sigma = home_rating.sigma + 100
        away_rating.sigma = away_rating.sigma + 100

        # So we don't evaluate on outcome
        home_clone = copy.deepcopy(home_rating)

        home_rating.newVarRating(away_rating, row['Score'], 1) #pone is 1 for home team - since default gamma is 0 this is irrelevant
        away_rating.newVarRating(home_clone, (1 - row['Score']), 0) 

        df_team.loc[df_team['team'] == row['HomeTeam'], 'steph_rating'] = home_rating
        df_team.loc[df_team['team'] == row['AwayTeam'], 'steph_rating'] = away_rating

for index, row in df_team.iterrows():
    print(f"{row['team']}:", end=" ")
    row['steph_rating'].printVals()