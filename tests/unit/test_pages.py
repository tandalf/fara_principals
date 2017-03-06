import os
from unittest import TestCase

import mock

from fara_principals.core.pages import __main_url__, PrincipalListPage
from fara_principals.exceptions import (
    BadPrincipalSchemaError, PageInstanceInfoNotFoundError
)

def get_data_dir():
    return os.path.normpath(os.path.join(__file__, '../../'))

print(get_data_dir())

class TestPrincipalListPage(TestCase):

    def setUp(self):
        self.normal_page_url_2 = \
            'https://efile.fara.gov/pls/apex/wwv_flow.show'
        with open(os.path.join(get_data_dir(), 'page2.html'), 'r') as f:
            self.normal_page_content_2 = f.read()
            self.page_context_2 = {
                "instance_id": 1, "flow_id": 171, "flow_step_id": 130,
                "worksheet_id": 1, "report_id": 1
            }
            self.list_page_2 = PrincipalListPage(self.normal_page_url_2, 
                content=self.normal_page_content_2, 
                page_context=self.page_context_2)

    def _main_page_context(self):
        return {
            "instance_id": '9488617858409', "flow_id": '171', 
            "flow_step_id": '130', "worksheet_id": '80340213897823017', 
            "report_id": '80341508791823021'
        }

    def _get_main_page_mock(self):
        with open(os.path.join(get_data_dir(), 'init.html'), 'r') as f:
            content = f.read()
            with mock.patch('fara_principals.core.pages.PrincipalListPage._build_main_page') \
            as page_mock:
                page_mock.return_value = None
                return PrincipalListPage(__main_url__, content=content)

    def test_is_main_page(self):
        #self.normal_page_content_2 is not the main page
        self.assertEqual(False, self.list_page_2.is_main_page())

        #todo: devise a way of testing if this is main page; this is more
        #more complicated.

    def test_get_page_context(self):
        self.assertEqual(self.page_context_2, 
            self.list_page_2.get_page_context())

        #test context for a mocked initial page
        main_page_mock = self._get_main_page_mock()
        self.assertEqual(self._main_page_context(), 
            main_page_mock.get_page_context())