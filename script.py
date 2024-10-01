from classes.GroupManager import GroupManager
from classes.UserManager import UserManager

user_manager = UserManager()
group_manager = GroupManager()

for j in range(1, 10000, 1000):
    info = user_manager.get_info_many([str(i) for i in range(j, j+1000)])
    for i in info:
        print(i)
