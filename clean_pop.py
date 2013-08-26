"""
Clean the population projection data at the state
level from the CONAPO (2010)
Proyecciones 2010-2030
Estimaciones 1990-2010
http://www.conapo.gob.mx/es/CONAPO/Proyecciones

Output:
Two files with population projections by
age group and sex will be placed in
the 'clean-data' directory
"""

import pandas as pd
import numpy as np

# Necessary for matching filenames downloaded from the
# CONAPO website
STATES = ["Aguascalientes", "BajaCalifornia", "BajaCaliforniaSur",
    "Campeche", "Chiapas", "Chihuahua", "Coahuila", "Colima",
    "DistritoFederal", "Durango", "Mexico", "Guanajuato",
    "Guerrero", "Hidalgo", "Jalisco", "Michoacan", "Morelos",
    "Nayarit", "NuevoLeon", "Oaxaca", "Puebla", "Queretaro",
    "QuintanaRoo", "SanLuisPotosi", "Sinaloa", "Sonora", "Tabasco",
    "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatan", "Zacatecas"]

# Each state is associated with a numeric code. Downloaded from:
# Catálogo Único de Claves de Áreas Geoestadísticas
# http://www.inegi.org.mx/geo/contenidos/geoestadistica/CatalogoClaves.aspx
INEGI_CODES = pd.read_csv('data/inegi_codes.csv')

def readStateXLSX(fileName, dirName):
    """
    read the appropiate worksheet containing the mid-year population
    data from an Excel file
    """
    # Are we reading the 1990-2009 or the 2010-2030 data?
    if dirName == 'state-indicators':
        years = range(1990, 2010)
        length = 21 #1990 to 2009
    else:
        years = range(2010, 2031)
        length = 22 #2010 to 2030, one extra year
    xlsxfile = pd.ExcelFile("data/" + dirName + "/" + fileName + ".xlsx")
    data = xlsxfile.parse('Indicadores demográficos', 
                          index_col = None, header = None)
    # Skip the first four rows that contain metadata
    df_xlsx = data.iloc[4:7, 1:length]
    df_xlsx = df_xlsx.transpose()
    df_xlsx.columns = ['Total', 'Men', 'Women']
    df_xlsx['Year'] = years
    df_xlsx['State'] = state
    return df_xlsx

def groupAge(sex, data, dirName, state):
    """
    Group DataFrame containg mid-year population data
    by 5 year age groups
    """
    # Data from 1990-2009 or 2010-2030?
    if dirName == "state-indicators":
        length = 21
        years = range(1990, 2010)
    else:
        length = 22
        years = range(2010, 2031)
    # read only the appropiate rows
    # The worksheet contains data for men at the top and women at the top
    if sex == "Males":
        df_xlsx = data.iloc[5:115, 1:length]
    else:
        df_xlsx = data.iloc[119:229, 1:length]
    ages = range(0, 110)
    # We want the data by 5 year age groups
    bins = [x for x in range(-1, 85, 5)]
    # No one lives to be 200
    bins.append(200)
    df_xlsx['AgeGroup'] = pd.cut(ages, bins = bins)
    df_xlsx = df_xlsx.replace(["(-1, 4]", "(4, 9]", "(9, 14]", "(14, 19]", 
                               "(19, 24]", 
                               "(24, 29]", "(29, 34]", "(34, 39]", "(39, 44]", 
                               "(44, 49]", 
                               "(49, 54]", "(54, 59]", "(59, 64]", "(64, 69]", 
                               "(69, 74]", 
                               "(74, 79]","(79, 84]", "(84, 200]"], 
                              ["0-4", "5-9","10-14","15-19","20-24", "25-29", 
                               "30-34", "35-39",
                               "40-44", "45-49", "50-54","55-59", "60-64",
                               "65-69","70-74","75-79","80-84", "85plus"])
    df_xlsx = df_xlsx.groupby("AgeGroup").sum()
    df_xlsx = df_xlsx.transpose()
    df_xlsx = pd.DataFrame(df_xlsx.stack())
    df_xlsx.columns = [sex]
    df_xlsx['Year'] = np.repeat(years, 18)
    df_xlsx = df_xlsx.reset_index()
    del df_xlsx['level_0'] 
    # Add the ugly state file name defined in STATES
    df_xlsx['State'] = state
    return df_xlsx
    
def readAgeXLXS(state, dirName):
    """
    Read the Excel file with the mid-year population data by age
    """
    xlsxfile = pd.ExcelFile("data/" + dirName + "/" + state + ".xlsx")
    data = xlsxfile.parse('Población media', 
                          index_col = None, header = None)
    return data
    
# Read the total mid-year population data for each year
pop = pd.DataFrame()
for state in STATES:
    pop = pop.append(readStateXLSX(state, 'state-indicators'))
    pop = pop.append(readStateXLSX(state, 'state-projections'))
# Add the fips number for each state
pop = pd.merge(pop, INEGI_CODES)
del pop['State']
pop[['Men', 'Total', 'Women']] = \
  pop[['Men', 'Total', 'Women']].apply(lambda col: np.round(col).astype(int))
pop.to_csv("clean-data/state-population.csv", index = False)

# Read the mid-year population data by age and group them
pop_agegroups = pd.DataFrame()
for state in STATES:
    df_males = groupAge("Males", readAgeXLXS(state, "state-indicators"), 
                            "state-indicators", state)
    df_females = groupAge("Females", readAgeXLXS(state, "state-indicators"), 
                              "state-indicators", state)
    df = pd.merge(df_males, df_females, on = ["AgeGroup", "Year", "State"], 
                  how='outer')
    df['Total'] = df.Males + df.Females
    pop_agegroups = pop_agegroups.append(df)
    df_males = groupAge("Males", readAgeXLXS(state, "state-projections"), 
                            "state-projections", state)
    df_females = groupAge("Females", readAgeXLXS(state, "state-projections"), 
                              "state-projections", state)
    df = pd.merge(df_males, df_females, on = ["AgeGroup", "Year", "State"], 
                  how='outer')
    df['Total'] = df.Males + df.Females
    pop_agegroups = pop_agegroups.append(df)

# Add the fips number corresponding to each state
pop_agegroups = pd.merge(pop_agegroups, INEGI_CODES)
# Remove the state filename used for joining the inegi codes 
# from the conapo excel files
del pop_agegroups['State']
pop_agegroups.to_csv("clean-data/state-population-age-groups.csv", index = False)
