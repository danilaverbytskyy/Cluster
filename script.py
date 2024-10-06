from classes.GroupManager import GroupManager
from classes.UserManager import UserManager
from database.GroupService import GroupService
from database.UserGroupService import UserGroupService
from database.UserService import UserService
from constants import DB_URL

user_manager = UserManager()
group_manager = GroupManager()
group_service = GroupService(DB_URL, GroupManager())
user_service = UserService(DB_URL, UserManager())
user_group_service = UserGroupService(DB_URL)

limit = 50
for j in range(1, limit, 500):
    user_service.add_users([str(i) for i in range(j, j + 500)])
    for vk_id in range(j, j + 500):
        subscriptions = user_manager.get_subscriptions(str(vk_id))
        if subscriptions is None or len(subscriptions['groups']['items']) == 0:
            continue
        group_ids = subscriptions['groups']['items']
        group_service.add_groups([str(elem) for elem in group_ids[0:500]])
        user_group_pairs = [(vk_id, group_id) for group_id in group_ids]
        user_group_service.add_user_groups(user_group_pairs)
