import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as shc
import pandas as pd

# Взято отсюда
# https://habr.com/ru/post/468295/
# Дендограмма, но  она не очень подходит
    # непонятна структура данных
    #  и непонятно как сделать из простых цифр зависимости


# Import Data
df = pd.read_csv('https://raw.githubusercontent.com/selva86/datasets/master/USArrests.csv')

# Plot
plt.figure(figsize=(8, 4), dpi= 80)  
plt.title("USArrests Dendograms", fontsize=22)

dend = shc.dendrogram(shc.linkage(df[['Murder', 'Assault', 'UrbanPop', 'Rape']], method='ward'), labels=df.State.values, color_threshold=100)  

# мой пример данных
# dend = shc.dendrogram(shc.linkage([ '1.1', '1.2', '1.3',' 1.4', '1.5', '2.1',' 2.2', '2.3', '2.4', '2.5' ], method='ward'), color_threshold=100, orientation='right')  

plt.xticks(fontsize=12)
plt.show()