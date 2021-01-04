from random import randint


class Appoint():
    def __init__(self, project_id):
        self.project_id = project_id

    def appoint_reviewer(self, gl, mr_iid, reviewer_id):
        # назначает ревьюера на мерж реквест
        project = gl.projects.get(self.project_id, lazy=True)
        editable_mr = project.mergerequests.get(mr_iid, lazy=True)
        editable_mr.assignee_id = reviewer_id
        editable_mr.save()

    def appoint_reviewer_random(self, members_db, gl, mr_iid):
        # назначает рандомного ревьюера на мерж реквест
        max_range = len(members_db) - 1
        random_number_in_range = randint(0, max_range)
        reviewer_id = members_db[random_number_in_range][0]
        self.appoint_reviewer(gl, mr_iid, reviewer_id)