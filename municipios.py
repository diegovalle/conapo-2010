import pandas as pd
import numpy as np
import pdb

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


def read_colmex(sheet, year):
    xlsxfile = pd.ExcelFile("data/" + "colmex" + "/" + str(year) + "total" + ".xls")
    data = xlsxfile.parse(sheet,
                          index_col=None, header=None, skiprows = 9, skip_footer = 1)
    data = data[pd.notnull(data[0])]
    data = data.iloc[0:len(data), 0:3]
    data['Year'] = year
    data.columns = ['Code', 'MunName', 'Population', 'Year']
    del data['MunName']
    data['Sex'] = {
        'Total': 'Total',
        'Hombres': 'Males',
        'Mujeres' : 'Females',
    }[sheet]
    return data

df_colmex = pd.DataFrame()
for year in range(1990, 2010):
    df_colmex = df_colmex.append(read_colmex("Total", year))
    df_colmex = df_colmex.append(read_colmex("Hombres", year))
    df_colmex = df_colmex.append(read_colmex("Mujeres", year))

#df[['Code', 'Population']] = df[['Code', 'Population']].apply(lambda col: np.round(col).astype(int))
#df[['Code', 'Population']] = df[['Code', 'Population']].apply(lambda col: col.astype(float))
df_colmex.Population[df_colmex.Year > 2005] = np.nan
df_colmex.to_csv('clean-data/municipio-population1990-2009.csv',
        encoding='utf-8',
        index = False)



df_conapo = pd.DataFrame()
#rows with data star from the 17th row
offset = 16
#2010-2030 excluding the colums for sex, year, etc
ncols = 25
for file in STATES:
    xlsxfile = pd.ExcelFile("data/" + "municipalities" + "/" + file + ".xlsx")
    data = xlsxfile.parse(file,
                          index_col=None, header=None)


    #Get rid of all the blank rows
    data = data[pd.notnull(data[4])]



    for i in range(offset, len(data), 5):
        x = pd.DataFrame(data.iloc[(i):(i + 5), 4:ncols].sum())
        x['Code'] = data.iloc[(i)][0]#.astype(int)
        x['Sex'] = sex(data.iloc[(i)][2])
        x['Year'] = years
        df_conapo = df_conapo.append(x)

df_conapo .columns = ['Population', 'Code', 'Sex', 'Year']
df_conapo [['Population', 'Code']] = \
        df_conapo [['Population', 'Code']].\
        apply(lambda col: np.round(col).astype(int))

df_conapo .to_csv('clean-data/municipio-population2010-2030.csv',
        encoding='utf-8',
        index = False)


df = df_colmex.append(df_conapo)
df = df.sort(['Code', 'Sex', 'Year'])
df['Code2'] = df['Code']
#Replace San Ignacio Cerro Gordo with Arandas to match the population data
df.Code2[df.Code2 == 14125] = 14008
#Tulum was created from Solidaridad
df.Code2[df.Code2 == 23009] = 23008
#Bacalar was created from Othón P Blanco
df.Code2[df.Code2 == 23010] = 23004
del df['Code']
#pdb.set_trace()
df= df.groupby(['Code2', 'Sex', 'Year']).aggregate(np.sum)
df = pd.DataFrame(df).reset_index()

df.rename(columns={'Code2': 'Code'}, inplace=True)

df['Population'] = df.groupby(['Code', 'Sex'])['Population'] \
    .apply(lambda x: pd.Series.interpolate(x, method = 'spline'))
#df = df.interpolate()
df[['Code', 'Population']] = df[['Code', 'Population']].apply(lambda col: np.round(col).astype(int))
df.to_csv('clean-data/municipio-population1990-2030.csv',
        encoding='utf-8',
        index = False)