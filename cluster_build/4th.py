import psycopg2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from datetime import datetime

from constants import DB_PASSWORD

# Конфигурация подключения к БД
DB_CONFIG = {
    "dbname": "cluster",
    "user": "postgres",
    "password": DB_PASSWORD,
    "host": "localhost",
    "port": "5432"
}


def get_db_connection():
    """Устанавливаем соединение с таймаутом"""
    try:
        return psycopg2.connect(**DB_CONFIG, connect_timeout=5)
    except Exception as e:
        print(f"Ошибка подключения: {e}")
        return None


def load_user_data(limit=5000):
    """Загружаем данные пользователей"""
    conn = get_db_connection()
    if not conn:
        return pd.DataFrame()

    try:
        query = f"""
        SELECT 
            user_vk_id,
            followers_count,
            last_seen
        FROM 
            users
        WHERE 
            followers_count IS NOT NULL
            AND last_seen IS NOT NULL
        ORDER BY 
            RANDOM()
        LIMIT {limit}
        """
        return pd.read_sql(query, conn)
    finally:
        conn.close()


def preprocess_data(df):
    """Подготовка данных для кластеризации"""
    # Заполняем пропуски
    df['followers_count'] = df['followers_count'].fillna(0)

    # Преобразуем last_seen в дни с последнего визита
    df['last_seen'] = pd.to_datetime(df['last_seen'])
    df['days_since_last_seen'] = (datetime.now() - df['last_seen']).dt.days

    # Логарифмируем followers_count для нормализации
    df['log_followers'] = np.log1p(df['followers_count'])

    return df


def cluster_users(df):
    """Кластеризация пользователей"""
    if df.empty:
        print("Нет данных для группировки")
        return

    # Выбираем признаки для кластеризации
    X = df[['log_followers', 'days_since_last_seen']]

    # Масштабируем данные
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Кластеризация (фиксируем 4 кластера)
    kmeans = KMeans(n_clusters=4, random_state=42)
    df['cluster'] = kmeans.fit_predict(X_scaled)

    # Визуализация
    plt.figure(figsize=(12, 8))

    # Цвета для кластеров
    colors = ['red', 'blue', 'green', 'purple']

    for cluster, color in zip(range(4), colors):
        cluster_data = df[df['cluster'] == cluster]
        plt.scatter(
            cluster_data['days_since_last_seen'],
            cluster_data['followers_count'],
            c=color,
            label=f'Группа {cluster}',
            alpha=0.5
        )

    plt.title('Группировка пользователей по подписчикам и активности')
    plt.xlabel('Дней с последнего визита')
    plt.ylabel('Количество подписчиков (логарифмическая шкала)')
    plt.yscale('log')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Статистика по кластерам
    print("\nСтатистика по группам:")
    stats = df.groupby('cluster').agg({
        'followers_count': ['mean', 'median', 'count'],
        'days_since_last_seen': ['mean', 'median']
    })
    print(stats)


if __name__ == "__main__":
    # Загружаем данные (5000 случайных пользователей)
    user_data = load_user_data(limit=5000)

    if not user_data.empty:
        # Предобработка данных
        processed_data = preprocess_data(user_data)

        # Кластеризация и визуализация
        cluster_users(processed_data)
    else:
        print("Не удалось загрузить данные")