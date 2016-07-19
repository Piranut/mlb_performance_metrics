import unicodecsv
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import defaultdict




college_playing = pd.read_csv('CollegePlaying.csv')


# print(college_playing['schoolID'])
college_count = college_playing['schoolID'].value_counts()


college_count[:20].plot(kind='barh',rot =0)
plt.show()