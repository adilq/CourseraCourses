import pandas as pd
import numpy as np
f = open('testing.txt', 'w')
pd.set_option('display.max_rows', None, 'display.max_columns', None)

def get_rid_of_parens(City_name):
    import re
    # Search for opening bracket in the name followed by
    # any characters repeated any number of times
    if re.search('\(.*', City_name):
  
        # Extract the position of beginning of pattern
        pos = re.search(' \(.*', City_name).start()
  
        # return the cleaned name
        return City_name[:pos]
  
    else:
        # if clean up needed return the same name
        return City_name
    
def get_rid_of_numbers(country):
    import re
    if re.search('[0-9]', country):
        pos = re.search('[0-9]', country).start()
        
     # return the cleaned name
        return country[:pos]
    else:
        # if clean up needed return the same name
        return country

def answer_zero():
    Energy = pd.read_excel('assets/Energy Indicators.xls', header=17, skipfooter=38, na_values='...', keep_default_na=True, usecols='C:F', names=['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable'])
    Energy['Country'] = Energy['Country'].apply(get_rid_of_parens)
    Energy['Country'] = Energy['Country'].apply(get_rid_of_numbers)
    Energy['Energy Supply'] = Energy['Energy Supply'].apply(lambda x: x*1000000)

    Energy.replace({'Country':{"Republic of Korea": "South Korea",
        "United States of America": "United States",
        "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
        "China, Hong Kong Special Administrative Region": "Hong Kong"}}, inplace=True)
    Energy = Energy.set_index('Country')

    GDP = pd.read_csv('assets/world_bank.csv', header=2)
    GDP.replace({'Country Name': {"Korea, Rep.": "South Korea", 
                            "Iran, Islamic Rep.": "Iran",
                            "Hong Kong SAR, China": "Hong Kong"}}, inplace=True)

    GDP = GDP.rename(columns={'Country Name': 'Country'})
    GDP = GDP.set_index("Country")

    ScimEn = pd.read_excel('assets/scimagojr-3.xlsx', index_col='Country')
    
    ans = pd.merge(Energy, GDP.loc[:, '2006':'2015'], right_index=True, left_index=True, how='inner')
    ans = pd.merge(ScimEn, ans, right_index=True, left_index=True, how='inner').drop('Region', axis=1)
    
    return ans

def answer_one():
    return answer_zero().iloc[:15]

def answer_two():
    Energy = pd.read_excel('assets/Energy Indicators.xls', header=17, skipfooter=38, na_values='...', keep_default_na=True, usecols='C:F', names=['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable'])
    Energy['Country'] = Energy['Country'].apply(get_rid_of_parens)
    Energy['Country'] = Energy['Country'].apply(get_rid_of_numbers)
    Energy['Energy Supply'] = Energy['Energy Supply'].apply(lambda x: x*1000000)

    Energy.replace({'Country':{"Republic of Korea": "South Korea",
        "United States of America": "United States",
        "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
        "China, Hong Kong Special Administrative Region": "Hong Kong"}}, inplace=True)
    Energy = Energy.set_index('Country')

    GDP = pd.read_csv('assets/world_bank.csv', header=2)
    GDP.replace({'Country Name': {"Korea, Rep.": "South Korea", 
                            "Iran, Islamic Rep.": "Iran",
                            "Hong Kong SAR, China": "Hong Kong"}}, inplace=True)

    GDP = GDP.rename(columns={'Country Name': 'Country'})
    GDP = GDP.set_index('Country')

    ScimEn = pd.read_excel('assets/scimagojr-3.xlsx', index_col='Country')
    
    ans1 = len(Energy)
    ans = pd.merge(ScimEn, Energy, right_index=True, left_index=True, how='inner')
    ans = pd.merge(ans, GDP.loc[:, '2006':'2015'], right_index=True, left_index=True, how='inner')
    ans2 = len(ans)
    
    return ans1 - ans2 + 15

def answer_three():
    df = answer_one()
    
    all_GDP = df.loc[:, '2006':'2015']
    all_GDP['Average GDP'] = all_GDP.mean(axis=1)
    
    avg_GDP = all_GDP['Average GDP'].sort_values(ascending=False).iloc[:15]
    return avg_GDP

def answer_four():
    df = answer_one()
    avg_GDP = answer_three()
    country_name = list(avg_GDP.index)[5]
    difference = df.loc[country_name]['2015'] - df.loc[country_name]['2006']
    return difference

def answer_five():
    df = answer_one()
    e_supp_per_cap = df['Energy Supply per Capita']
    return e_supp_per_cap.mean()

def answer_six():
    df = answer_one()
    renewable = df['% Renewable'].sort_values(ascending=False)
    return renewable.index[0], renewable.iloc[0]

def answer_seven():
    df = answer_one()
    df['Citation Ratio'] = df['Self-citations']/df['Citations']
    ratio = df['Citation Ratio'].sort_values(ascending=False)
    return ratio.index[0], ratio.iloc[0]

def answer_eight():
    df = answer_one()
    df['Population Estimate'] = df['Energy Supply']/df['Energy Supply per Capita']
    pop_est = df['Population Estimate'].sort_values(ascending=False)

    return pop_est.index[2]

def answer_nine():
    df = answer_one()

    df['Population Estimate'] = df['Energy Supply']/df['Energy Supply per Capita']
    df['Citable Docs per Capita'] = df['Citable documents']/df['Population Estimate']
    
    return df['Citable Docs per Capita'].corr(df['Energy Supply per Capita'])

def plot9():
    import matplotlib as plt
   
    top15 = answer_one()
    top15['PopEst'] = top15['Energy Supply'] / top15['Energy Supply per Capita']
    top15['Citable docs per Capita'] = top15['Citable documents'] / top15['PopEst']
    top15.plot(x='Citable docs per Capita', y='Energy Supply per Capita', kind='scatter', xlim=[0, 0.0006])

def func10(x, median_renew):
    if x > median_renew:
        return 1
    return 0

def answer_ten():
    df = answer_one()
    median_renew = df['% Renewable'].median()
    df['HighRenew'] = df['% Renewable'].apply(func10, args=[median_renew])
    HighRenew = df['HighRenew']
    return HighRenew
    
def answer_eleven():
    df = answer_one()
    df['PopEst'] = df['Energy Supply'] / df['Energy Supply per Capita']

    ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    
    df['Continent'] = pd.Series(ContinentDict)
    
    df_new = df.groupby('Continent').agg({"PopEst" :(np.size, np.sum, np.mean, np.std)})

    return df_new

def answer_twelve():
    top15 = answer_one()
    ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    
    top15['Continent'] = pd.Series(ContinentDict)
    top15['% Renewable'] = pd.cut(top15["% Renewable"], 5)
    top15.reset_index(inplace=True)
    top15 = top15.groupby(["Continent", "% Renewable"]).agg(lambda x : np.size(x)).dropna()
    return top15['Country']

def comma(num):
    '''Add comma to every 3rd digit. Takes int or float and
    returns string.'''
    if type(num) == int:
        return '{:,}'.format(num)
    elif type(num) == float:
        return '{:,.2f}'.format(num) # Rounds to 2 decimal places
    else:
        print("Need int or float as input to function comma()!")

def answer_thirteen():
    top15 = answer_one()
    top15['PopEst'] = top15['Energy Supply'] / top15['Energy Supply per Capita']
    return top15['PopEst'].apply(comma)

if __name__ == '__main__':
    print(answer_three())


