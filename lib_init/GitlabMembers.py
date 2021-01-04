class GitlabMembers():
    def __init__(self, group, cursor):
        self.group = group
        self.cursor = cursor

    def group_members_gitlab(self):
        # получение списка юзеров группы из гитлаба
        members_gitlab = dict()
        members = self.group.members.list()
        for member in members:
            members_gitlab[member.id] = member.name
        return members_gitlab

    def insert_update_member_for_bd(self, members_gitlab):
        # добавление или обновление участников
        for member_id, member_name in members_gitlab.items():
            member_id = str(member_id)
            sqlstr = 'update members set Name = \'' + member_name + '\' WHERE ID = ' + member_id + ' IF @@ROWCOUNT=0 INSERT INTO members(ID,Name)VALUES(' + member_id + ', \'' + member_name + '\')'
            self.cursor.execute(sqlstr)
        self.cursor.commit()

    def group_mebmers_db(self):
        # получение списка юзеров группы из базы данных
        members_db = []
        sqlstr = 'select * from members where id <> 31'
        self.cursor.execute(sqlstr)
        for member in self.cursor:
            members_db.append(member)
        return members_db

    def members_run(self):
        members_gitlab = self.group_members_gitlab()
        self.insert_update_member_for_bd(members_gitlab)
        return self.group_mebmers_db()