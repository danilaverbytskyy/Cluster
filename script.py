from Models.QueryBuilder import QueryBuilder


vk_url = input("Введите ссылку на страницу ВКонтакте: \n")
query_builder = QueryBuilder()
friends = query_builder.get_user_friends(vk_url)
print(friends)
