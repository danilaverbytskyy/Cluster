from sqlalchemy import create_engine
from models import *
#
# engine = create_engine("sqlite:///cluster.db")
# Base.metadata.create_all(bind=engine)
#
# # Создание движка для PostgreSQL
db_url = "postgresql+psycopg2://postgres:3dh1z6@localhost:5432/cluster"
engine = create_engine(db_url)
Base.metadata.create_all(bind=engine)
