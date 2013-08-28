# -*- coding: utf-8 -*-
import pandas as pd

def test_state_pop():
    """
    Compare state populations with the values in the Excel files
    """
    def assert_pop(df, sex, state_name, year):
        return(df[sex][(df.StateName == state_name) &
                       (df.Year == year)])
    df = pd.read_csv("clean-data/state-population.csv")
    assert_pop(df, 'Total', 'Aguascalientes', 1995) == 921048
    assert_pop(df, 'Total', 'Baja California Sur', 2009) == 626900
    assert_pop(df, 'Males', 'México', 2008) == 7336800
    assert_pop(df, 'Females', 'Zacatecas', 2030) == 898437
    assert_pop(df, 'Females', 'Sinaloa', 2015) == 1511413


def test_agegroup_pop():
    """
    Compare the age group populations with manually computed
    sums from the Excel files
    """
    def assert_pop(df, sex, state_name, year, age_group):
        return(df[sex][(df.StateName == state_name) &
                       (df.Year == year) &
                       (df.AgeGroup == age_group)])
    df = pd.read_csv("clean-data/state-population-age-groups.csv")
    assert_pop(df, 'Males', 'Chiapas', 2019, '80-84') == 16986
    assert_pop(df, 'Males', 'Michoacán', 2030, '15-19') == 204978
    assert_pop(df, 'Females', 'Nuevo León', 1998, '30-34') == 157366
    assert_pop(df, 'Total', 'Tabasco', 2005, '50-54') == 38958 + 38868

