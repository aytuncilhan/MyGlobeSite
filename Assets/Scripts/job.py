from datetime import date

class Job:
    def __init__(self):
        self.id = "0000"
        self.publish_date = "1970-01-01"
        self.title = ""
        self.grade = ""
        self.deadline = "1970-01-01"

    def __eq__(self, other):
        if isinstance(other, Job):
            return (
                self.id == other.id and
                self.title == other.title and
                self.grade == other.grade
            )
