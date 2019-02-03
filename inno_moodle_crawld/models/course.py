from dataclasses import dataclass
from typing import List

from crawld import models


@dataclass
class Course(models.Model):
    id: str
    name: str


class CourseMapper(models.Mapper):
    __object_class__ = Course
    __page_url__ = 'https://moodle.innopolis.university/'

    id = models.pipe() \
        .select('a').first_element() \
        .attribute('href') \
        .function(
            lambda x, **k: x.replace('https://moodle.innopolis.university/course/view.php?id=', '')
        )
    name = models.pipe().select('a').first_element().text()

    def get_dom_node_list(self, soup, **context):
        return soup.select('div.hidden-xs-down.visible-phone > div > div.media-body > h4')


@dataclass
class CourseAssignment:
    id: str
    name: str


class CourseAssignmentMapper(models.Mapper):
    __object_class__ = CourseAssignment

    id = models.pipe() \
        .attribute('href') \
        .function(lambda x, **k: x.replace('https://moodle.innopolis.university/mod/assign/view.php?id=', ''))
    name = models.pipe().text()


@dataclass
class CourseDetail(models.Model):
    id: str
    assignments: List[CourseAssignment]


class CourseDetailMapper(models.Mapper):
    __object_class__ = CourseDetail
    __page_url__ = 'https://moodle.innopolis.university/course/view.php?id={course_id}'

    id = models.pipe().context_attribute('course_id')
    assignments = models.pipe(required=False) \
        .select('.activity.assign.modtype_assign .activityinstance') \
        .select('a', many=True).every_first_element() \
        .spawn(CourseAssignmentMapper, many=True).every_first_element()


class CourseManager(models.Manager):
    list = Course
    detail = CourseDetail
