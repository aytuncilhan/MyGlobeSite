from datetime import date

class Job:
    def __init__(self, id, publish_date, deadline, grade, title):
        self.id = id
        self.publish_date = publish_date
        self.deadline = deadline
        self.grade = grade
        self.title = title