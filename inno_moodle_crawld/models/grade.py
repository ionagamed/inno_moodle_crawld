from dataclasses import dataclass
from typing import Optional

from crawld import models


@dataclass(frozen=True, eq=True)
class Grade(models.Model):
    value: str
    name: str
    course_id: Optional[str] = None
    description: Optional[str] = None
    range: Optional[str] = None
    feedback: Optional[str] = None


class GradeMapper(models.Mapper):
    __object_class__ = Grade
    __page_url__ = 'https://moodle.innopolis.university/course/user.php?mode=grade&id={course_id}&user={user_id}'

    course_id = models.pipe().context_attribute('course_id')
    value = models.pipe().select('.column-grade').first_element().text().strip()
    name = models.pipe().select('.gradeitemheader').first_element().text().strip()
    description = models.pipe(required=False).select('.gradeitemdescription').first_element().text().strip()
    range = models.pipe(required=False).select('.column-range').first_element().text().strip()
    feedback = models.pipe(required=False).select('.column-feedback').first_element().text().strip()

    def get_dom_node_list(self, soup, **context):
        return [
            x for x in soup.select('.grade-report-user tbody tr')
            if x.select('.column-grade')
        ]


class GradeManager(models.Manager):
    list = Grade
