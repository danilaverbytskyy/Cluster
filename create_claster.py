import matplotlib
matplotlib.use('TkAgg')  # Установка бэкэнда
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

# Загрузка данных
df = pd.read_csv("users.csv")
print(df.head())

# Подготовка данных
X = df[['followers_count']].copy()
X = X.dropna()

# Подготовка для визуализации "локтя"
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, random_state=0)
    kmeans.fit(X)
    wcss.append(kmeans.inertia_)

# Построение графика
sns.set()
plt.plot(range(1, 11), wcss)
plt.title('Selecting the Number of Clusters using the Elbow Method')
plt.xlabel('Clusters')
plt.ylabel('WCSS')
plt.show()  # Или plt.savefig('elbow_method.png') для сохранения
