import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from constants import DB_PASSWORD
from models import Base


class DatabaseManager:
    def __init__(self):
        self._dsn = f"postgresql://postgres:{DB_PASSWORD}@localhost:5432/cluster"
        self.connection = None
        self.cursor = None
        self.session = None
        self.engine = None

        self._connect()

    def _connect(self):
        """Устанавливает соединение с базой данных."""
        try:
            # Подключение через psycopg2
            self.connection = psycopg2.connect(
                dbname="cluster",
                user="postgres",
                password=DB_PASSWORD,
                host="localhost",
                port="5432"
            )
            self.cursor = self.connection.cursor()

            # Подключение через SQLAlchemy
            self.engine = create_engine(self._dsn, pool_pre_ping=True)
            Session = sessionmaker(bind=self.engine)
            self.session = Session()

            print("✅ Подключение к базе данных успешно.")
        except psycopg2.Error as e:
            print(f"❌ Ошибка подключения к PostgreSQL: {e}")
        except Exception as e:
            print(f"❌ Общая ошибка: {e}")

    def execute_query(self, query: str, params=None):
        """Выполняет SQL-запрос с защитой от SQL-инъекций."""
        try:
            self.cursor.execute(query, params)
            self.connection.commit()  # Коммит транзакции
        except psycopg2.Error as e:
            self.connection.rollback()  # Откат транзакции в случае ошибки
            print(f"❌ Ошибка выполнения запроса: {e}")

    def fetch_all(self, query: str, params=None):
        """Выполняет SELECT-запрос и возвращает все результаты."""
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            print(f"❌ Ошибка выполнения запроса: {e}")
            return None

    def close(self):
        """Закрывает соединение с базой данных."""
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
            if self.session:
                self.session.close()
            if self.engine:
                self.engine.dispose()
            print("🔒 Соединение с базой данных закрыто.")
        except psycopg2.Error as e:
            print(f"❌ Ошибка при закрытии соединения: {e}")
