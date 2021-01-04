from random import choice
from collections import Counter
import sys


class Appoint():
    def __init__(self, project_id):
        self.project_id = project_id

    def appoint_reviewer(self, not_empty_merge_requests, gl, mr_iid,
                         reviewer_id):
        # назначает ревьюера на мерж реквест
        project = gl.projects.get(self.project_id, lazy=True)
        editable_mr = project.mergerequests.get(mr_iid, lazy=True)
        editable_mr.assignee_id = reviewer_id
        editable_mr.save()
        not_empty_merge_requests[mr_iid] = reviewer_id
        return not_empty_merge_requests

    def appoint_reviewer_random(self, members_db, not_empty_merge_requests, gl,
                                mr_iid):
        # назначает рандомного ревьюера на мерж реквест
        count_requests_user = Counter(not_empty_merge_requests.values())
        busy_men = list(
            filter(lambda id_user: count_requests_user[id_user] >= 2,
                   count_requests_user.keys()))
        free_men = list(set(members_db) ^ set(busy_men))
        if not free_men:
            sys.exit()
        else:
            reviewer_id = choice(free_men)
            not_empty_merge_requests = self.appoint_reviewer(
                not_empty_merge_requests, gl, mr_iid, reviewer_id)
            return not_empty_merge_requests
