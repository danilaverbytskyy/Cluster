from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base


class DatabaseManager:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(bind=self.engine)
        self.Session = sessionmaker(autoflush=False, bind=self.engine)
