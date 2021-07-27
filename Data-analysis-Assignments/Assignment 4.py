import pandas as pd
import numpy as np
import scipy.stats as stats
import re

def noParens(City_name):
    # Search for opening bracket in the name followed by
    # any characters repeated any number of times
    if re.search('[\[\*\+\(]', City_name):
  
        # Extract the position of beginning of pattern
        pos = re.search('[\[\*\+\(]', City_name).start()
  
        # return the cleaned name
        return City_name[:pos]
  
    else:
        # if clean up needed return the same name
        return City_name

def sepTeams(city):
    if city == np.nan:
        return np.nan
    teams_loc = re.findall('[A-Z0-9][a-z0-9]*\ [A-Z][a-z0-9]*|[A-Z0-9][a-z0-9]*', city)

    for i in range(len(teams_loc)):
        if not re.search('Sox', teams_loc[i]):
            teams_loc[i] = getTeamName(teams_loc[i])

    return teams_loc
    
def getTeamName(li):
    li = re.sub('\*', '', li)
    if not re.search('Sox', li):
        li = re.sub('[\w.]* ', '', li)
    elif re.search('White', li):
        return 'White Sox'
    elif re.search('Red', li):
        return 'Red Sox'
    li = li.strip()
    return li

def getWinLossRatio(city, league, df):
    wins, losses, wl = 0,0, []
    if city[league] != []:
        for team in city[league]:
            wins = float(df.at[team,'W'])
            losses = float(df.at[team,'L'])
            wl.append(wins/(wins+losses))
        return np.mean(wl)
    else:
        return np.NaN

def format_df(df_list, cities):
    cities.rename(columns={'Population (2016 est.)[8]': 'Population'}, inplace=True)
    cities = cities.applymap(noParens)
    cities[['NHL', 'NBA', 'MLB', 'NFL']]  = cities[['NHL', 'NBA', 'MLB', 'NFL']].applymap(sepTeams)

    for df in df_list:
        df = df[df['year'] == 2018]

        df['team name'] = df['team'].apply(lambda x: re.split(' ', x))
        df['team name'] = df['team name'].apply(getTeamName)

        if df['League'].all() == 'NFL':
            df['mask'] = df['L'].apply(lambda x: x.isnumeric())
            df = df[df['mask']]

        df = df[df['team name'] != 'Division']
        df.set_index('team name', inplace=True)

def nhl_correlation():
    global cities
    global nhl_df 

    Big4 = 'NHL'

    cities.rename(columns={'Population (2016 est.)[8]': 'Population'}, inplace=True)
    cities = cities.applymap(noParens).replace("", np.nan).replace('—', np.nan).dropna(subset=[Big4])
    cities[Big4]  = cities[Big4].apply(sepTeams)

    nhl_df = nhl_df[nhl_df['year'] == 2018]
    nhl_df['team name'] = nhl_df['team'].apply(getTeamName)

    nhl_df = nhl_df[['team name', 'W', 'L']]
    nhl_df = nhl_df[nhl_df['L'] != nhl_df['W']]
    nhl_df.set_index('team name', inplace=True)
    

    cities['Winloss'] = cities.apply(getWinLossRatio, args =(Big4, nhl_df), axis=1)

    ans = cities[['Winloss', 'Population']].astype({'Winloss': float, 'Population': int})
    win_loss_by_region = ans['Winloss'] # pass in win/loss ratio from nhl_df in the same order as cities["Metropolitan area"]
    population_by_region = ans['Population'] # pass in metropolitan area population from cities

    assert len(population_by_region) == len(win_loss_by_region), "Q1: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q1: There should be 28 teams being analysed for NHL"
    
    return stats.pearsonr(population_by_region, win_loss_by_region)[0]

def nba_correlation():
    global cities
    global nba_df

    Big4 = 'NBA'

    cities.rename(columns={'Population (2016 est.)[8]': 'Population'}, inplace=True)
    cities = cities.applymap(noParens).replace("", np.nan).replace('—', np.nan).dropna(subset=[Big4])
    cities[Big4]  = cities[Big4].apply(sepTeams)

    nba_df = nba_df[nba_df['year'] == 2018]
    nba_df['team name'] = nba_df['team'].apply(noParens).apply(getTeamName)

    nba_df = nba_df[['team name', 'W', 'L']]
    nba_df = nba_df[nba_df['L'] != nba_df['W']]
    nba_df.set_index('team name', inplace=True)
    

    cities['Winloss'] = cities.apply(getWinLossRatio, args =(Big4, nba_df), axis=1)

    ans = cities[['Winloss', 'Population']].astype({'Winloss': float, 'Population': int})
    win_loss_by_region = ans['Winloss'] # pass in win/loss ratio from nba_df in the same order as cities["Metropolitan area"]
    population_by_region = ans['Population'] # pass in metropolitan area population from cities

    assert len(population_by_region) == len(win_loss_by_region), "Q1: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q1: There should be 28 teams being analysed for NHL"
    
    return stats.pearsonr(population_by_region, win_loss_by_region)[0]

def mlb_correlation():
    global cities
    global mlb_df

    Big4 = 'MLB'

    cities.rename(columns={'Population (2016 est.)[8]': 'Population'}, inplace=True)
    cities = cities.applymap(noParens).replace("", np.nan).replace('—', np.nan).dropna(subset=[Big4])
    cities[Big4]  = cities[Big4].apply(sepTeams)

    mlb_df = mlb_df[mlb_df['year'] == 2018]
    mlb_df['team name'] = mlb_df['team'].apply(noParens).apply(getTeamName)

    mlb_df = mlb_df[['team name', 'W', 'L']]
    mlb_df = mlb_df[mlb_df['L'] != mlb_df['W']]
    mlb_df.set_index('team name', inplace=True)
    

    cities['Winloss'] = cities.apply(getWinLossRatio, args =(Big4, mlb_df), axis=1)

    ans = cities[['Winloss', 'Population']].astype({'Winloss': float, 'Population': int})
    win_loss_by_region = ans['Winloss'] # pass in win/loss ratio from mlb_df in the same order as cities["Metropolitan area"]
    population_by_region = ans['Population'] # pass in metropolitan area population from cities

    assert len(population_by_region) == len(win_loss_by_region), "Q1: Your lists must be the same length"
    assert len(population_by_region) == 26, "Q1: There should be 28 teams being analysed for NHL"
    
    return stats.pearsonr(population_by_region, win_loss_by_region)[0]

def nfl_correlation():
    global cities
    global nfl_df

    Big4 = 'NFL'

    cities.rename(columns={'Population (2016 est.)[8]': 'Population'}, inplace=True)
    cities = cities.applymap(noParens).replace("", np.nan).replace('—', np.nan).replace('— ', np.nan).dropna(subset=[Big4])
    cities[Big4]  = cities[Big4].apply(sepTeams)

    nfl_df = nfl_df[nfl_df['year'] == 2018]
    nfl_df['team name'] = nfl_df['team'].apply(noParens).apply(getTeamName)

    nfl_df = nfl_df[['team name', 'W', 'L']]
    nfl_df = nfl_df[nfl_df['L'] != nfl_df['W']]
    nfl_df.set_index('team name', inplace=True)
    

    cities['Winloss'] = cities.apply(getWinLossRatio, args =(Big4, nfl_df), axis=1)

    ans = cities[['Winloss', 'Population']].astype({'Winloss': float, 'Population': int})
    win_loss_by_region = ans['Winloss'] # pass in win/loss ratio from mlb_df in the same order as cities["Metropolitan area"]
    population_by_region = ans['Population'] # pass in metropolitan area population from cities

    assert len(population_by_region) == len(win_loss_by_region), "Q1: Your lists must be the same length"
    assert len(population_by_region) == 29, "Q1: There should be 28 teams being analysed for NHL"
    
    return stats.pearsonr(population_by_region, win_loss_by_region)[0]

def sports_team_performance():
    global cities, nhl_df, nba_df, mlb_df, nfl_df
    format_df([nhl_df, nba_df, mlb_df, nfl_df], cities)


pd.set_option('display.max_rows', None, 'display.max_columns', None)
nhl_df=pd.read_csv("assets/nhl.csv")
nba_df=pd.read_csv("assets/nba.csv")
mlb_df=pd.read_csv("assets/mlb.csv")
nfl_df=pd.read_csv("assets/nfl.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]

print(nhl_correlation())
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]

print(nba_correlation())
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]

print(mlb_correlation())
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]

print(nfl_correlation())