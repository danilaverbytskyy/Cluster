from classes.GroupManager import GroupManager
from classes.UserManager import UserManager
from database.GroupService import GroupService
from database.UserGroupService import UserGroupService
from database.UserService import UserService
from constants import DB_URL

USER_COUNT_LIMIT = 10

user_manager = UserManager()
group_manager = GroupManager()
group_service = GroupService(DB_URL, GroupManager())
user_service = UserService(DB_URL, UserManager())
user_group_service = UserGroupService(DB_URL)

user_count = 0
for j in range(1, 7777777777, 500):
    user_ids = [str(user_id) for user_id in range(j, j+500)]
    for user_id in user_ids:
        subscriptions = user_manager.get_subscriptions(user_id)
        if subscriptions is None:
            continue
        group_ids = subscriptions['groups']['items']
        user_group_pairs = [(user_id, group_id) for group_id in group_ids]   
        if user_group_pairs is None or len(user_group_pairs) == 0:
            continue
        
        user_service.add_users([str(user_id)])
        group_service.add_groups([str(elem) for elem in group_ids[0:500]])
        user_group_service.add_user_groups(user_group_pairs)

        user_count += 1
        if user_count >= USER_COUNT_LIMIT:
            break
    if user_count >= USER_COUNT_LIMIT:
        break
