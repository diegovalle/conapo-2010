#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
from __future__ import unicode_literals
import pandas as pd
import numpy as np
#import pytest

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


def read_state_xlsx(file_name, dir_name):
    """
    read the appropiate worksheet containing the mid-year population
    data from an Excel file
    """
    # Are we reading the 1990-2009 or the 2010-2030 data?
    if dir_name == 'state-indicators':
        years = range(1990, 2010)
        length = 21  # 1990 to 2009
    else:
        years = range(2010, 2031)
        length = 22  # 2010 to 2030, one extra year
    xlsxfile = pd.ExcelFile("data/" + dir_name + "/" + file_name + ".xlsx")
    data = xlsxfile.parse('Indicadores demográficos',
                          index_col=None, header=None)
    # Skip the first four rows that contain metadata
    df_xlsx = data.iloc[4:7, 1:length]
    df_xlsx = df_xlsx.transpose()
    df_xlsx.columns = ['Total', 'Males', 'Females']
    df_xlsx['Year'] = years
    df_xlsx['State'] = file_name
    return df_xlsx


def group_age(sex, data, dir_name, state):
    """
    Group DataFrame containg mid-year population data
    by age into 5 year age groups
    """
    ugly_agegroups = ["(-1, 4]", "(4, 9]", "(9, 14]", "(14, 19]",
                      "(19, 24]", "(24, 29]", "(29, 34]",
                      "(34, 39]", "(39, 44]", "(44, 49]",
                      "(49, 54]", "(54, 59]", "(59, 64]", "(64, 69]",
                      "(69, 74]", "(74, 79]", "(79, 84]", "(84, 200]"]
    nice_agegroups = ["0-4", "5-9", "10-14", "15-19", "20-24", "25-29",
                      "30-34", "35-39", "40-44", "45-49", "50-54",
                      "55-59", "60-64", "65-69", "70-74", "75-79",
                      "80-84", "85plus"]
    # Data from 1990-2009 or 2010-2030?
    if dir_name == "state-indicators":
        length = 21
        years = range(1990, 2010)  # 1990-2009
    else:
        length = 22
        years = range(2010, 2031)  # 2010-2030
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
    df_xlsx['AgeGroup'] = pd.cut(ages, bins=bins)
    df_xlsx = df_xlsx.replace(ugly_agegroups,
                              nice_agegroups)
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


def read_age_xlsx(state, dir_name):
    """
    Read the Excel file with the mid-year population data by age
    """
    xlsxfile = pd.ExcelFile("data/" + dir_name + "/" + state + ".xlsx")
    data = xlsxfile.parse('Población media',
                          index_col=None, header=None)
    return data


def test_state_pop(df):
    """
    Compare state populations with the values in the Excel files
    """
    assert df.Total[(df.StateName == 'Aguascalientes') &
                    (df.Year == 1995)] == 921048
    assert df.Total[(df.StateName == 'Baja California Sur') &
                    (df.Year == 2009)] == 626900
    assert df.Males[(df.StateName == 'México') &
                    (df.Year == 2008)] == 7336800
    assert df.Females[(df.StateName == 'Zacatecas') &
                      (df.Year == 2030)] == 898437
    assert df.Females[(df.StateName == 'Sinaloa') &
                      (df.Year == 2015)] == 1511413


def test_agegroup_pop(df):
    """
    Compare the age group populations with manually computed
    sums from the Excel files
    """
    assert df.Males[(df.StateName == 'Chiapas') &
                    (df.Year == 2019) &
                    (df.AgeGroup == '80-84')] == 16986
    assert df.Males[(df.StateName == 'Michoacán') &
                    (df.Year == 2030) &
                    (df.AgeGroup == '15-19')] == 204978
    assert df.Females[(df.StateName == 'Nuevo León') &
                      (df.Year == 1998) &
                      (df.AgeGroup == '30-34')] == 157366
    assert df.Total[(df.StateName == 'Tabasco') &
                    (df.Year == 2005) &
                    (df.AgeGroup == '50-54')] == 38958 + 38868


def process_state(state, timeframe):
    """
    Clean the age data for one state
    """
    df_males = group_age("Males",
                         read_age_xlsx(state, timeframe),
                         timeframe, state)
    df_females = group_age("Females",
                           read_age_xlsx(state, timeframe),
                           timeframe, state)
    df = pd.merge(df_males, df_females, on=["AgeGroup", "Year", "State"],
                  how='outer')
    df['Total'] = df.Males + df.Females
    return(df)


def add_inegi_codes(df, save, file_name):
    """
    Each state is assigned a numeric code by the
    INEGI (Mexican Statistical Agency) similar to
    FIPS
    """
    # Add the fips number for each state
    df = pd.merge(df, INEGI_CODES)
    # Remove the state filename used for joining the inegi codes
    # from the conapo excel files
    del df['State']
    # No use in using decimal points since we are measuring
    # people
    df[['Males', 'Total', 'Females']] = \
        df[['Males', 'Total', 'Females']].\
        apply(lambda col: np.round(col).astype(int))
    if save:
        df.to_csv("clean-data/" + file_name, index=False)
    return(df)


def main():
    """
    First clean the total population and then do the same
    for the age grouped data
    """
    pop = pd.DataFrame()
    pop_agegroups = pd.DataFrame()
    # Read the *total* mid-year population data for each year
    # The data comes in two files 1990-2009 (indicators) and
    # 2010-2030 (projections)
    for state in STATES:
        pop = pop.append(read_state_xlsx(state, 'state-indicators'))
        pop = pop.append(read_state_xlsx(state, 'state-projections'))
    pop = add_inegi_codes(pop, True,
                          file_name="state-population.csv")

    # Read the mid-year population data by *age*, and group them
    for state in STATES:
        df = process_state(state, "state-indicators")
        pop_agegroups = pop_agegroups.append(df)
        df = process_state(state, "state-projections")
        pop_agegroups = pop_agegroups.append(df)
    pop_agegroups = add_inegi_codes(
        pop_agegroups, True,
        file_name="state-population-age-groups.csv")
    # Unit tests
    test_state_pop(pop)
    test_agegroup_pop(pop_agegroups)


if __name__ == "__main__":
    main()
