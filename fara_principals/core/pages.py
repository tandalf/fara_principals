import copy

import requests
from scrapy import Selector

from fara_principals.exceptions import (
    BadPrincipalSchemaError, PageInstanceInfoNotFoundError
)

__main_url__ = \
    'https://efile.fara.gov/pls/apex/f?p=171:130:0::NO:RP,130:P130_DATERANGE:N'

__default_page_context__ = {
    "instance_id": None, "flow_id": None, "flow_step_id": None,
    "worksheet_id": None, "report_id": None
}

class PrincipalListPage:
    """
    Page class with useful helpers responsible for navigating a paginated
    page containing Foreign Principal information.

    Args:
        url(str): url of the page being accessed

    Keyword Args:
        content(str): (optional) content of the page whose structure is to be
            parsed for principal entries. If this value is None, the 
            special case for an initial page load will be run.

        page_context(dict): (optional) a dict containing contextual info
            about a page
    """

    def __init__(self, url, content=None, page_context={}, *args, **kwargs):
        self._url = url
        self._content = content

        self._page_context = None
        self._page_context = page_context or self.get_page_context()

        if self.is_main_page():
            self._build_main_page()
        else:
            self._build_normal_page()

    def is_main_page(self):
        """
        Returns:
            bool: True if the url for this page is that of the main 
            active foreign principal web page.
        """
        return self._url == __main_url__

    def get_page_context(self):
        """
        Returns:
            dict: a dict containing details including the server-tracked
            page instance id and other server-tracked details which are 
            necessary to make further requests to the server.

        Raises:
            PageinstanceInfoNotFoundError: when an important page context
            variable is not found in the loaded html page.
        """
        #print(self._content)
        if self._page_context:
            return self._page_context

        context = copy.deepcopy(__default_page_context__)
        context["instance_id"] = self._page_instance_id()
        context["flow_id"] = self._page_flow_id()
        context["flow_step_id"] = self._page_flow_step_id()
        context["worksheet_id"] = self._page_worksheet_id()
        context["report_id"] = self._page_report_id()
        
        return context

    def _page_instance_id(self):
        try:
            instance_id = Selector(text=self._content).\
                xpath('//input[@name="p_instance"]/@value').extract()[0]
            return str(instance_id)
        except Exception:
            raise PageInstanceInfoNotFoundError("page data {} not found".\
                format("instance_id"))

    def _page_flow_id(self):
        try:
            flow_id = Selector(text=self._content).\
                xpath('//input[@name="p_flow_id"]/@value').extract()[0]
            return str(flow_id)
        except Exception:
            raise PageInstanceInfoNotFoundError("page data {} not found".\
                format("flow_id"))

    def _page_flow_step_id(self):
        try:
            flow_step_id = Selector(text=self._content).\
                xpath('//input[@name="p_flow_step_id"]/@value').extract()[0]
            return str(flow_step_id)
        except Exception:
            raise PageInstanceInfoNotFoundError("page data {} not found".\
                format("flow_step_id"))

    def _page_worksheet_id(self):
        try:
            page_selector = Selector(text=self._content)
            return str(page_selector.xpath(
                '//input[@id="apexir_WORKSHEET_ID"]/@value').extract()[0])
        except Exception:
            raise PageInstanceInfoNotFoundError("page data {} not found".\
                format("worksheet_id"))

    def _page_report_id(self):
        try:
            page_selector = Selector(text=self._content)
            return str(page_selector.xpath(
                '//input[@id="apexir_REPORT_ID"]/@value').extract()[0])
        except Exception:
            raise PageInstanceInfoNotFoundError("page data {} not found".\
                format("report_id"))

    def _build_main_page(self):
        """
        Builds the necessary internal structures for the first page since
        the first page has some extra requirements
        """
        pass

    def _build_normal_page(self):
        pass

    def next_page_form_data(self):
        """
        Contructs a dict which contains the form data needed to request the
        next page.

        Returns:
            dict: next page form data
        """
        pass

    def next_page_url(self):
        """
        Constructs a url for the request of the next page to be retrieved

        Returns:
            str: the url of the next page to be which would be opened if
            the next button had been clicked in the browser.
        """
        pass

    def next_page_cookie(self):
        """
        Returns:
            dict: a cookie in form of a dict which will be used to make
            requests for the next page.
        """
        pass

    def principals(self):
        """
        Returns:
            list: a list of str urls for pages which Principals can be 
            scraped from.
        """
        pass


class ForeignPrincipal:

    def __init_(self, url=None, country=None, state=None, address=None, 
        reg_number=None, principal_name=None, principal_reg_date=None, 
        reg_date=None, registrant=None, exhibits=[], partial_data=None, 
        *args, **kwargs):

        self._dict_info = None
        if partial_data:
            self._dict_info = partial_data
        else:
            self._dict_info = {
                "url": url, "country_name": country, "state": state, 
                "address": address, "reg_number": reg_number, 
                "principal_name": principal_name, 
                "principal_reg_date": principal_reg_date, 
                "reg_date": reg_date, "exhibits": exhibits
            }

    def validate_data(self):
        """
        Confirms that certain keys are present in the dict returned by 
        `self.to_dict`

        Raises:
            BadPrincipalSchemaError: raised when certain fields(keys) are 
            unavailable or when required contrains on the schema are not met.

        Note: this method is to be called when it has been populated with 
        it's exhibit info.
        """
        pass

    def validate_partial(self):
        """
        Confirms that certain keys are present given that this instance 
        represents a pricipal whose full data has not yet been collected.

        Raises:
            BadPrincipalSchemaError: raised when certain fields(keys) are 
            unavailable or when required contrains on the schema are not met.
        """
        pass

    def partial_dict(self):
        """
        Returns:
            dict: a dict representation of the principal without it's
            exhibit data.
        """
        pass

    def is_partial(self):
        """
        Returns:
            bool: True if the principal this instance represents does not
            yet contain all it's information including it's exibit data.

        Note: a principal is usually still partial when it has been 
        populate from the list page but not from its detail page.
        """
        pass

    def to_dict(self):
        """
        Returns:
            dict: a dict representation of the Principal instance
        """
        pass

    def to_json(self):
        """
        Returns:
            str: a json string representation of the Principal instance
        """
        pass