import numpy as np
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
import missingno as msno

import warnings
warnings.filterwarnings('ignore')


data = pd.read_csv('vacancies.csv')

#cleaning
data.dropna(inplace = True)
data['experience'] = data['experience'].str.replace('Требуемый опыт работы:','').str.strip()
data['experience'] = data['experience'].str.replace('лет','').str.strip()
data['experience'] = data['experience'].str.replace('не требуется','0').str.strip()
data['experience'] = data['experience'].str.replace('года','').str.strip()
data['experience'] = data['experience'].str.replace('более','').str.strip()

data.drop('link', axis=1, inplace=True)

data.rename(columns={'tags': 'skills'}, inplace=True)

data['salary'] = data[['lower_salary', 'upper_salary']].mean(axis=1)
data.drop(['lower_salary', 'upper_salary'], axis=1, inplace=True)

# модель, предсказывающая зарплату в зависимости от скиллов и опыта
