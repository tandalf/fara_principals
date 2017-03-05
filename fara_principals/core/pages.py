import copy

import requests

__init_url__ = "https://efile.fara.gov/pls/apex/f?p=171:1:0:::::"

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
    """

    def __init__(self, url, content=None, *args, **kwargs):
        self._url = url
        self._content = content

        self._is_initial_page = None

        if (self._url == __init_url__) and (not self._content):
            self._is_initial_page = True
            self._build_initial_page()
        else:
            self._is_initial_page = False
            self._build_normal_page()

    def _build_initial_page(self):
        """
        Builds the necessary internal structures for the first page since
        the first page has some extra requirements
        """
        pass

    def _build_normal_page(self):
        pass

    def next_page_request(self):
        """
        Constructs a scrapy request for the next page to be retrieved

        Returns:
            str: the url of the next page to be which would be opened if
            the next button had been clicked in the browser.
        """
        pass

    def principals(self):
        """
        Returns:
            list: a list of urls for pages which Principals can be scraped
            from.
        """
        pass

    def _country_ids(self):
        """
        Returns:
            list: a list of html string id for each contry in a page.

        Note: This ids can be used for searching for the principal urls
        for a given country on the page. This is because, the ids of the
        principal table data DOM is derived from it's country's html id.
        """
        pass


class ForeignPrincipal:

    def __init_(self, url=None, country=None, state=None, address=None, 
        reg_num=None, foreign_principal=None, date=None, registrant=None, 
        exhibits=[], *args, **kwargs):

        self._dict_info = copy.deepcopy(kwargs)

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