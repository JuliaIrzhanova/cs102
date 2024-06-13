import numpy as np
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
import missingno as msno
from sklearn.preprocessing import LabelEncoder
import pickle

import warnings
warnings.filterwarnings('ignore')

data = pd.read_csv('data.csv')

print(data.columns)
print(data['Metro station'].unique())

# кодирование значений
label = LabelEncoder()
dicts = {}

label.fit(data['Apartment type'].drop_duplicates()) #задаем список значений для кодирования
dicts['Apartment type'] = list(label.classes_)
data['Apartment type'] = label.transform(data['Apartment type']) #заменяем значения из списка кодами закодированных элементов

label.fit(data['Metro station'].drop_duplicates())
dicts['Metro station'] = list(label.classes_)
data['Metro station'] = label.transform(data['Metro station'])

label.fit(data['Region'].drop_duplicates())
dicts['Region'] = list(label.classes_)
data['Region'] = label.transform(data['Region'])

label.fit(data['Renovation'].drop_duplicates())
dicts['Renovation'] = list(label.classes_)
data['Renovation'] = label.transform(data['Renovation'])


with open('label_encoder.pkl', 'wb') as f:
    pickle.dump(label, f)

with open('label_encoder.pkl', 'rb') as f:
   le_loaded = pickle.load(f)

le_loaded.fit(dicts['Apartment type'])
test['Apartment type'] = le_loaded.transform(test['Apartment type'])

le_loaded.fit(dicts['Metro station'])
test['Metro station'] = le_loaded.transform(test['Metro station'])

le_loaded.fit(dicts['Region'])
test['Region'] = le_loaded.transform(test['Region'])

le_loaded.fit(dicts['Renovation'])
test['Renovation'] = le_loaded.transform(test['Renovation'])