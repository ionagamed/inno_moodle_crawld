from dataclasses import dataclass

from crawld import models


@dataclass
class Grade(models.Model):
    course_id: str
    value: str
    name: str


class GradeMapper(models.Mapper):
    __object_class__ = Grade
    __page_url__ = 'https://moodle.innopolis.university/course/user.php?mode=grade&id={course_id}&user={user_id}'

    course_id = models.pipe().context_attribute('course_id')
    value = models.pipe().select('.column-grade', first=True).text()
    name = models.pipe().select('.column-itemname', first=True).text()

    def get_dom_node_list(self, soup, **context):
        return [
            x for x in soup.select('.grade-report-user tbody tr')
            if x.select('.column-grade')
        ]
