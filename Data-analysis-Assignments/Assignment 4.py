import pandas as pd
import numpy as np
import scipy.stats as stats
import re

nhl_df=pd.read_csv("assets/nhl.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]

def noParens(City_name):
    # Search for opening bracket in the name followed by
    # any characters repeated any number of times
    if re.search('\[', City_name):
  
        # Extract the position of beginning of pattern
        pos = re.search('\[', City_name).start()
  
        # return the cleaned name
        return City_name[:pos]
  
    else:
        # if clean up needed return the same name
        return City_name

def sepTeams(league):
    teams = []
    for city in league:
        city = noParens(city)
        teams_loc = re.findall('[A-Z0-9][a-z0-9]*', city)
        teams.extend(teams_loc)
    return teams
    

def nhl_correlation(): 
    cities.columns[1] = 'Population'

    cities.applymap(noParens)
    teams  = sepTeams(cities['NHL'])
    nhl_df = nhl_df[nhl_df['year'] == '2018']
    
    
    win_loss_by_region = [] # pass in win/loss ratio from nhl_df in the same order as cities["Metropolitan area"]
    population_by_region = [] # pass in metropolitan area population from cities
    
    for i in range(len(teams)):
        population_by_region.append(cities['Population'].iloc[i])

    assert len(population_by_region) == len(win_loss_by_region), "Q1: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q1: There should be 28 teams being analysed for NHL"
    
    return stats.pearsonr(population_by_region, win_loss_by_region)

if __name__ == '__main__':
    print(nhl_df)
