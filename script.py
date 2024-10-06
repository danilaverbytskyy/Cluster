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

# with Session(autoflush=False, bind=engine) as db:
#     groups_info = group_manager.get_info_by_ids([str(i) for i in range(500)])
#     db_groups_info = []
#     for single_group_information in groups_info:
#         group = Group(
#             vk_id=single_group_information['id'],
#             name=single_group_information['name'],
#             members_count=(single_group_information['members_count'] if 'members_count' in single_group_information.keys() else 0),
#             is_closed=bool(single_group_information['is_closed'])
#         )
#         db_groups_info.append(group)
#     db.add_all(db_groups_info)
#     db.commit()

with Session(autoflush=False, bind=engine) as db:
    users_info = user_manager.get_info([str(i) for i in range(1500, 2000)])
    db_users_info = []
    for single_user_information in users_info:
        user = User(
            vk_id=single_user_information['id'],
            first_name=single_user_information['first_name'],
            last_name=single_user_information['last_name'],
            sex=single_user_information['sex'],
            is_closed=single_user_information['is_closed']
        )
        db_users_info.append(user)
    db.add_all(db_users_info)
    db.commit()
