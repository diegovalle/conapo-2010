import pandas as pd
import numpy as np
#import pdb

# Necessary for matching filenames downloaded from the
# CONAPO website
STATES = ["Aguascalientes", "BajaCalifornia", "BajaCaliforniaSur",
          "Campeche", "Chiapas", "Chihuahua", "Coahuila", "Colima",
          "DistritoFederal", "Durango", "Mexico", "Guanajuato",
          "Guerrero", "Hidalgo", "Jalisco", "Michoacan", "Morelos",
          "Nayarit", "NuevoLeon", "Oaxaca", "Puebla", "Queretaro",
          "QuintanaRoo", "SanLuisPotosi", "Sinaloa", "Sonora", "Tabasco",
          "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatan", "Zacatecas"]
years = range(2010, 2031)


def sex(x):
    '''
    Switch statement to translate sex
    '''
    return {
        'Ambos': 'Total',
        'Hombres': 'Males',
        'Mujeres' : 'Females',
    }[x]

df = pd.DataFrame()
for file in STATES:
    xlsxfile = pd.ExcelFile("data/" + "municipalities" + "/" + file + ".xlsx")
    data = xlsxfile.parse(file,
                          index_col=None, header=None)


    #Get rid of all the blank rows
    data = data[pd.notnull(data[4])]

    #rows with data star from the 17th row
    offset = 16
    #2010-2030 excluding the colums for sex, year, etc
    ncols = 25

    for i in range(offset, len(data), 5):
        x = pd.DataFrame(data.iloc[(i):(i + 5), 4:ncols].sum())
        x['Code'] = data.iloc[(i)][0]#.astype(int)
        x['Sex'] = sex(data.iloc[(i)][2])
        x['Year'] = years
        df = df.append(x)

df.columns = ['Population', 'Code', 'Sex', 'Year']
df[['Population', 'Code']] = \
        df[['Population', 'Code']].\
        apply(lambda col: np.round(col).astype(int))

df.to_csv('clean-data/municipio-population.csv',
        encoding='utf-8',
        index = False)
#pdb.set_trace()