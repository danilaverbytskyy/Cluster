SELECT g.*
FROM groups g
JOIN user_groups ug ON g.id = ug.group_id;
