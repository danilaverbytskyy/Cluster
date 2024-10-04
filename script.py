from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import *
from classes.GroupManager import GroupManager
from classes.UserManager import UserManager

engine = create_engine("sqlite:///cluster.db")
Base.metadata.create_all(bind=engine)
Session = sessionmaker(autoflush=False, bind=engine)

user_manager = UserManager()
group_manager = GroupManager()

user_id = user_manager.get_id('https://vk.com/allidoistrytrytry')

with Session(autoflush=False, bind=engine) as db:
    users_info = user_manager.get_info([str(i) for i in range(500)])
    db_users_info = []
    for single_user_information in users_info:
        user = User(
            id=single_user_information['id'],
            first_name=single_user_information['first_name'],
            last_name=single_user_information['last_name'],
            sex=single_user_information['sex'],
            is_closed=single_user_information['is_closed']
        )
        db_users_info.append(user)
    db.add_all(db_users_info)
    db.commit()


