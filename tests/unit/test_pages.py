import os
from unittest import TestCase

import mock

from fara_principals.core.pages import (
    __main_url__, PrincipalListPage, ExhibitPage
)
from fara_principals.exceptions import (
    InvalidPrincipalError, PageInstanceInfoNotFoundError
)

def get_data_dir():
    return os.path.normpath(os.path.join(__file__, '../../'))

class TestPrincipalListPage(TestCase):

    def setUp(self):
        self.page2_principal_reg_nums = [
            "6065", "5926", "2244", "2310", "5483", "5839", "3712", "6336", 
            "5430", "1995", "1995", "5299", "5712", "5712", "5840"
        ]
        self.page2_principal_names = [
            "SOCAR USA, subsidiary of State Oil Company of Azerbaijan Republic (SOCAR)",
            "Embassy of the Republic of Azerbaijan", 
            "Government of the Commonwealth of The Bahamas",
            "Bahamas Ministry of Tourism",
            "Kingdom of Bahrain, Embassy",
            "Ministry of Foreign Affairs Kingdom of Bahrain",
            "Kingdom of Bahrain",
            "Organization for Peace and Justice through Cassidy and Associates",
            "Government of the People's Republic of Bangladesh, Embassy",
            "Barbados Industrial Development Corporation",
            "Barbados Tourist Board",
            "Invest Barbados",
            "Open Joint Stock Company Belarusian Potash Company (OJSC BPC)",
            "Open Joint Stock Company Belaruskali (OJSC Belaruskali)",
            "Flanders Tourism Board"
        ]
        self.next_page_url = 'https://efile.fara.gov/pls/apex/wwv_flow.show'
        self.normal_page_url_2 = \
            'https://efile.fara.gov/pls/apex/wwv_flow.show'
        self.principals_count_2 = 15
        with open(os.path.join(get_data_dir(), 'page2.html'), 'r') as f:
            self.normal_page_content_2 = f.read()
            self.page_context_2 = {
                "instance_id": '9488617858409', "flow_id": "171", 
                "flow_step_id": "130", "worksheet_id": "80340213897823017", 
                "report_id": "80341508791823021", "page": 2
            }
            self.list_page_2 = PrincipalListPage(self.normal_page_url_2, 
                content=self.normal_page_content_2, 
                page_context=self.page_context_2)

    def _main_page_context(self):
        return {
            "instance_id": '9488617858409', "flow_id": '171', 
            "flow_step_id": '130', "worksheet_id": '80340213897823017', 
            "report_id": '80341508791823021', "page": 1
        }

    def _main_page_form_data(self):
        return {
            "p_request": "APXWGT",
            "p_instance": "9488617858409",
            "p_flow_id": "171",
            "p_flow_step_id": "130",
            "p_widget_num_return": "15",
            "p_widget_name": "worksheet",
            "p_widget_mod": "ACTION",
            "p_widget_action": "PAGE",
            "p_widget_action_mod": "pgR_min_row=1max_rows=15rows_fetched=15",
            "x01": "80340213897823017",
            "x02":"80341508791823021",
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

    def test_next_page_form_data(self):
        next_page_form_data = self._main_page_form_data()
        main_page_mock = self._get_main_page_mock()
        self.assertEqual(next_page_form_data, 
            main_page_mock.next_page_form_data())

        #test page 2
        next_page_form_data["p_widget_action_mod"] = \
            "pgR_min_row=16max_rows=30rows_fetched=15"
        self.assertEqual(next_page_form_data, 
            self.list_page_2.next_page_form_data())

    def test_next_page_url(self):
        self.assertEqual(self.next_page_url, self.list_page_2.next_page_url())

    def test_correct_number_of_partial_principals(self):
        self.assertEqual(self.principals_count_2, 
            len(self.list_page_2.partial_principals()))

    def test_correct_principal_reg_numbers_in_page(self):
        for principal in self.list_page_2.partial_principals():
            self.assertIn(principal.to_dict()["reg_number"], 
                self.page2_principal_reg_nums)

    def test_correct_principal_names_in_page(self):
        for principal in self.list_page_2.partial_principals():
            self.assertIn(principal.to_dict()["principal_name"], 
                self.page2_principal_names)


class TestExhibitPage(TestCase):

    def setUp(self):
        self.exhibit2_dates = [
            "05/25/2007", "03/03/1993"
        ]
        self.exhibit2_doc_urls = [
            "http://www.fara.gov/docs/4776-Exhibit-AB-20070525-9.pdf",
            "http://www.fara.gov/docs/4776-Exhibit-AB-19930303-D1Y2IS02.pdf"
        ]
        with open(os.path.join(get_data_dir(), 'exhibit_page1.html'), 'r') as f:
            self.exhibit_page = ExhibitPage(f.read())

    def test_page_contain_right_amount_of_exhibit(self):
        self.assertEqual(2, len(self.exhibit_page.exhibits()))

    def test_page_contains_right_dates(self):
        for exhibit in self.exhibit_page.exhibits():
            self.assertIn(exhibit.to_dict()["date_stamped"], 
                self.exhibit2_dates)

    def test_page_contains_right_urls(self):
        for exhibit in self.exhibit_page.exhibits():
            self.assertIn(exhibit.to_dict()["document_link"], 
                self.exhibit2_doc_urls)