import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.filterwarnings('ignore')


# Lectura del Dataset
data = pd.read_csv("data/iflow_data.csv")

data.head()
data.tail()

# Referencias 
# https://www.analyticsvidhya.com/blog/2022/07/step-by-step-exploratory-data-analysis-eda-using-python/