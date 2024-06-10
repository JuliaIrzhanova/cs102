import numpy as np
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
import missingno as msno

import warnings
warnings.filterwarnings('ignore')

data = pd.read_csv('data.csv')

print(data.isnull().sum())