import re
from html import unescape

import requests

from inno_moodle_crawld.models import CourseManager


class Client(object):
    def __init__(self, login=None, password=None):
        # if login and password and oauth_code:
        #     raise ValueError('You cannot specify all of: login, password, oauth_code')

        self.session = None
        self.user_id = None

        if login and password:
            self.auth_login_password(login, password)

    def auth_login_password(self, login, password):
        try:
            session = requests.Session()

            moodle_login_page = session.get(f'https://moodle.innopolis.university/login/index.php')
            sso_link = next(re.finditer(r'href="(.*?)" title="Innopolis University"',
                                        moodle_login_page.text)).group(1)
            sso_link = unescape(sso_link)
            sso_redirect = session.get(sso_link)
            form_submit_link = next(re.finditer(r' Login.submitLoginRequest\(\);" action="(.*?)"',
                                                sso_redirect.text)).group(1)
            form_submit_link = 'https://sso.university.innopolis.ru' + form_submit_link
            final_response = session.post(form_submit_link, data={
                'UserName': login,
                'Password': password,
                'Kmsi': 'true',
                'AuthMethod': 'FormsAuthentication'
            })
            # print(final_response.text)
            final_action = next(
                re.finditer(r'name="hiddenform" action="(.*?)"', final_response.text)).group(1)
            final_code = next(re.finditer(r'name="code" value="(.*?)"', final_response.text)).group(1)
            final_state = next(re.finditer(r'name="state" value="(.*?)"', final_response.text)).group(1)

            response = session.post(final_action, data={
                'code': final_code,
                'state': final_state
            }).text
            self.user_id = next(re.finditer(r'data-userid="(\d+?)"', response)).group(1)
            self.session = session
        except:
            raise ValueError('could not login')

    # proxies to actual models

    def get_course_list(self):
        return CourseManager.get_list(session=self.session)

    def get_course  (self, course_id):
        return CourseManager.get_detail(course_id=course_id, session=self.session)
