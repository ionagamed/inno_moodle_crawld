from dataclasses import dataclass
from crawld import models


@dataclass
class Assignment(models.Model):
    course_id: str
    name: str


class AssignmentMapper(models.Mapper):
    __object_class__ = Assignment
    __page_url__ = 'https://moodle.innopolis.university/course/view.php?id={course_id}'

    course_id = models.pipe().context_attribute('course_id')
    name = models.pipe().select('.instancename').text()

    def get_dom_node_list(self, soup, **context):
        return soup.select('.activity.assign.modtype_assign')
