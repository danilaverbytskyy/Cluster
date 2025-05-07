import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

from constants import DB_PASSWORD

# Конфигурация подключения к БД
DB_CONFIG = {
    "dbname": "cluster",
    "user": "postgres",
    "password":DB_PASSWORD,
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


def load_city_data(limit=7):
    """Загружаем данные по городам"""
    conn = get_db_connection()
    if not conn:
        return pd.DataFrame()

    try:
        query = f"""
        SELECT 
            city,
            COUNT(*) as users_count
        FROM 
            users
        WHERE 
            city IS NOT NULL
        GROUP BY 
            city
        ORDER BY 
            users_count DESC
        LIMIT {limit}
        """
        return pd.read_sql(query, conn)
    finally:
        conn.close()


def cluster_cities(df):
    """Кластеризация городов по количеству пользователей"""
    if df.empty:
        print("Нет данных для группировки")
        return

    # Преобразуем названия городов в числовые признаки
    ct = ColumnTransformer(
        [('encoder', OneHotEncoder(), ['city'])],
        remainder='passthrough'
    )

    X = ct.fit_transform(df[['city', 'users_count']])

    # Масштабируем данные
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X.toarray())

    # Кластеризация (фиксируем 4 кластера)
    kmeans = KMeans(n_clusters=7, random_state=42)
    df['cluster'] = kmeans.fit_predict(X_scaled)

    # Визуализация
    plt.figure(figsize=(12, 8))

    # Топ-20 городов для наглядности
    top_cities = df.sort_values('users_count', ascending=False).head(20)

    for cluster in sorted(df['cluster'].unique()):
        cluster_data = top_cities[top_cities['cluster'] == cluster]
        plt.bar(cluster_data['city'], cluster_data['users_count'], label=f'Группа {cluster}')

    plt.title('Группировка городов по количеству пользователей')
    plt.xlabel('Город')
    plt.ylabel('Количество пользователей')
    plt.xticks(rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Выводим статистику
    print("\nСтатистика по группам:")
    print(df.groupby('cluster').agg({
        'city': 'count',
        'users_count': ['mean', 'sum']
    }))


if __name__ == "__main__":
    city_data = load_city_data(limit=7)

    if not city_data.empty:
        cluster_cities(city_data)
    else:
        print("Не удалось загрузить данные")