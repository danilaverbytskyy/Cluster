from sqlalchemy import create_engine

from models import *

engine = create_engine("sqlite:///cluster.db")
Base.metadata.create_all(bind=engine)
