
def average_influenza_doses():
    import pandas as pd
    
    df = pd.read_csv('Data-analysis-Assignments/NISPUF17.csv')
    data = df[['CBF_01', 'P_NUMFLU']]
    
    breast_feeding = data[data['CBF_01'] == 1].dropna()
    non_breast_feeding = data[data["CBF_01"] == 2].dropna()
    
    avg_breast_feeding = breast_feeding['P_NUMFLU'].sum()/len(breast_feeding['P_NUMFLU'])
    avg_non_breast_feeding = non_breast_feeding['P_NUMFLU'].sum()/len(non_breast_feeding['P_NUMFLU'])
    
    return avg_breast_feeding, avg_non_breast_feeding 

def chickenpox_by_sex():
    import pandas as pd
    df = pd.read_csv('Data-analysis-Assignments/NISPUF17.csv')
    df = df[['P_NUMVRC', 'SEX', 'HAD_CPOX']]
    
    females = df[(df['P_NUMVRC'] >= 1) & (df['SEX'] == 2)]
    males = df[(df['P_NUMVRC'] >= 1) & (df['SEX'] == 1)]
    
    male_cpox = len(males[males['HAD_CPOX'] == 1])
    female_cpox = len(females[females['HAD_CPOX'] == 1])
    
    male_nopox = len(males[males['HAD_CPOX'] == 2])
    female_nopox = len(females[females['HAD_CPOX'] == 2])
    
    
    return {'male': male_cpox/male_nopox, 'female': female_cpox/female_nopox}

def corr_chickenpox():
    import scipy.stats as stats
    import numpy as np
    import pandas as pd
    df = pd.read_csv('Data-analysis-Assignments/NISPUF17.csv')
    
    df = df[["HAD_CPOX", 'P_NUMVRC']].dropna()
    df = df[df["HAD_CPOX"] <= 2]

    # here is some stub code to actually run the correlation
    corr, pval=stats.pearsonr(df["HAD_CPOX"],df["P_NUMVRC"])
    
    # just return the correlation
    return corr
print(corr_chickenpox())