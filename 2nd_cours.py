import psycopg2
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

from constants import DB_PASSWORD

# Параметры подключения к БД
DB_NAME = "cluster"
DB_USER = "postgres"
DB_PASSWORD = DB_PASSWORD
DB_HOST = "localhost"
DB_PORT = "5432"


# Подключение к PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn


# Загрузка данных из таблицы users
def load_data():
    conn = get_db_connection()
    query = """
    SELECT 
        user_vk_id,
        first_name,
        last_name,
        sex,
        is_closed,
        birth_date,
        city,
        last_seen,
        followers_count,
        occupation,
        relation,
        -- Вычисление возраста из birth_date (формат 'DD.MM.YYYY')
        CASE 
            WHEN birth_date ~ '^\d{2}\.\d{2}\.\d{4}$' THEN 
                EXTRACT(YEAR FROM AGE(NOW(), TO_DATE(birth_date, 'DD.MM.YYYY')))
            ELSE NULL 
        END AS age,
        -- Признак активности (дней с последнего визита)
        EXTRACT(DAY FROM NOW() - last_seen) AS days_since_last_seen
    FROM 
        users
    WHERE 
        is_closed = FALSE  -- Исключаем закрытые профили
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df


# Предобработка данных
def preprocess_data(df):
    # Заполнение пропусков
    df['age'].fillna(df['age'].median(), inplace=True)
    df['days_since_last_seen'].fillna(df['days_since_last_seen'].median(), inplace=True)
    df['followers_count'].fillna(0, inplace=True)

    # Преобразование категориальных признаков
    df['sex'] = df['sex'].map({1: 'female', 2: 'male', 0: 'unknown'}).fillna('unknown')
    df['city'] = df['city'].fillna('unknown')
    df['relation'] = df['relation'].fillna(0)  # 0 — статус неизвестен

    return df


# Кластеризация и визуализация
def cluster_and_visualize(df):
    # Выбор признаков
    features = df[['age', 'sex', 'city', 'relation', 'followers_count', 'days_since_last_seen']]

    # Пайплайн для обработки данных
    numeric_features = ['age', 'followers_count', 'days_since_last_seen']
    categorical_features = ['sex', 'city', 'relation']

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])

    X = preprocessor.fit_transform(features)

    # Метод локтя для определения оптимального k
    inertia = []
    for k in range(1, 11):
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(X)
        inertia.append(kmeans.inertia_)

    plt.figure(figsize=(10, 6))
    plt.plot(range(1, 11), inertia, marker='o')
    plt.xlabel('Number of clusters (k)')
    plt.ylabel('Inertia')
    plt.title('Elbow Method for Optimal k')
    plt.grid()
    plt.show()

    # Кластеризация (k=4)
    kmeans = KMeans(n_clusters=4, random_state=42)
    df['cluster'] = kmeans.fit_predict(X)

    # Визуализация 1: Возраст vs. Подписчики
    plt.figure(figsize=(12, 6))
    sns.scatterplot(
        x='age',
        y='followers_count',
        hue='cluster',
        data=df,
        palette='viridis',
        alpha=0.7
    )
    plt.title('Кластеры пользователей: Возраст vs. Подписчики')
    plt.xlabel('Возраст')
    plt.ylabel('Число подписчиков')
    plt.legend(title='Кластер')
    plt.show()

    # Визуализация 2: Распределение возраста по кластерам
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='cluster', y='age', data=df, palette='Set2')
    plt.title('Распределение возраста по кластерам')
    plt.xlabel('Кластер')
    plt.ylabel('Возраст')
    plt.show()

    # Визуализация 3: Состав кластеров по полу
    cluster_gender = pd.crosstab(df['cluster'], df['sex'], normalize='index') * 100
    cluster_gender.plot(kind='bar', stacked=True, figsize=(10, 6))
    plt.title('Распределение пола по кластерам (%)')
    plt.xlabel('Кластер')
    plt.ylabel('Доля (%)')
    plt.xticks(rotation=0)
    plt.legend(title='Пол')
    plt.show()

    # Статистика по кластерам
    cluster_stats = df.groupby('cluster').agg({
        'age': ['mean', 'median'],
        'sex': lambda x: x.mode()[0],
        'followers_count': 'mean',
        'days_since_last_seen': 'mean',
        'relation': lambda x: x.mode()[0]
    }).reset_index()

    print("Характеристики кластеров:\n", cluster_stats)


# Основной скрипт
if __name__ == "__main__":
    df = load_data()
    df = preprocess_data(df)
    cluster_and_visualize(df)