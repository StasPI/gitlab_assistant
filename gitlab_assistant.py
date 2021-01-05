from config.settings import config
from lib_init.connect_database import connect_db
from lib_init.GitlabMembers import GitlabMembers
from lib_init.Appoint import Appoint
from gitlab import Gitlab

# переменные
url = config['gitlab']['url']
token = config['gitlab']['token']
project = config['gitlab']['project']

db_driver = config['db']['db_driver']
db_server = config['db']['server']
db_database = config['db']['database']

version_branch = config['branch']['version']
user_story_branch = config['branch']['user_story']
bug_branch = config['branch']['bug']
'''
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Место подключение
'''
# курсор коннекта к базе данных
cursor = connect_db(db_driver, db_server, db_database)
gl = Gitlab(url, token)
gl.auth()
'''
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Исполнение основной логики
'''


def search_for_merge_requests(group):
    # сбор мерж реквестов пустых и назначенных
    empty_merge_requests_iid = dict()
    empty_merge_requests_author_id = dict()
    not_empty_merge_requests = dict()
    mr_all = group.mergerequests.list()
    for mr in mr_all:
        if str(mr.merged_at) == "None":
            if str(mr.assignee) == "None":
                empty_merge_requests_iid[mr.iid] = mr.target_branch
                empty_merge_requests_author_id[mr.iid] = [mr.author['id']]
            else:
                not_empty_merge_requests[mr.iid] = mr.assignee['id']
    return empty_merge_requests_iid, empty_merge_requests_author_id, not_empty_merge_requests


def brain_reviewer(group, members_db, gl):
    empty_merge_requests_iid, empty_merge_requests_author_id, not_empty_merge_requests = search_for_merge_requests(
        group)
    for mr_iid, target_branch in empty_merge_requests_iid.items():
        tb = target_branch.lower()[0]
        if tb == version_branch:
            # если вверсию то только Серега
            not_empty_merge_requests = appoint.appoint_reviewer(
                not_empty_merge_requests, gl, mr_iid, 31)
        elif tb == user_story_branch:
            not_empty_merge_requests = appoint.appoint_reviewer_random(
                members_db, not_empty_merge_requests,
                empty_merge_requests_author_id, gl, mr_iid)
        elif tb == bug_branch:
            not_empty_merge_requests = appoint.appoint_reviewer_random(
                members_db, not_empty_merge_requests,
                empty_merge_requests_author_id, gl, mr_iid)
        else:
            not_empty_merge_requests = appoint.appoint_reviewer_random(
                members_db, not_empty_merge_requests,
                empty_merge_requests_author_id, gl, mr_iid)


if __name__ == '__main__':
    for project_id in project:
        # подключение к проекту
        group = gl.projects.get(project_id)
        # инициализация класса обработки юзеров
        gm = GitlabMembers(group, cursor)
        # запуск полной обработки, возвращает актуальных юзеров
        members_db = gm.members_run()
        # инициализация класса назначения ревьюира
        appoint = Appoint(project_id)
        brain_reviewer(group, members_db, gl)