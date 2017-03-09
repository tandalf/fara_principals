import copy

import scrapy

from fara_principals.core.pages import PrincipalListPage, ExhibitPage
from fara_principals.core.principals import ForeignPrincipal, Exhibit

class ActivePrincipalsSpider(scrapy.Spider):
    name = 'active_principals'

    def start_requests(self):
        begin_url = 'https://efile.fara.gov/pls/apex/' + \
            'f?p=171:130:0::NO:RP,130:P130_DATERANGE:N'

        page = PrincipalListPage(begin_url)
        dict_cookies = page.main_page_cookie()

        return self.__class__._next_requests(page, dict_cookies)

    @classmethod
    def _next_requests(cls, page, cookies):
        next_page_request = cls._next_page_request(page, cookies)

        partial_principals = page.partial_principals()
        exhibit_requests = cls._exhibit_requests(partial_principals,
            cookies)

        return [next_page_request] + exhibit_requests

    @classmethod
    def _next_page_request(cls, page, cookies):
        next_page_url = page.next_page_url()
        page_context = page.get_page_context()

        next_page_form_data = page.next_page_form_data()
        next_page_context = copy.deepcopy(page_context)
        next_page_context["page"] = page_context["page"] + 1
        next_page_request = scrapy.FormRequest(url=next_page_url, 
            callback=cls.parse_principal_page, cookies=cookies,
            meta={"page_context": next_page_context}, dont_filter=True,
            method='POST', formdata=next_page_form_data)
        return next_page_request

    @classmethod
    def _exhibit_requests(cls, principals, cookies):
        exhibit_requests = []
        for partial_principal in principals:
            #print "\n\n\n\n"
            #print partial_principal.to_dict()
            exhibit_request = cls._exhibit_request(
                partial_principal, cookies)
            exhibit_requests.append(exhibit_request)

        return exhibit_requests

    @classmethod
    def _exhibit_request(cls, principal, cookies):
        partial_principal_dict = principal.to_dict()
        return scrapy.Request(url=partial_principal_dict["url"], 
            meta=dict(partial_principal_dict=partial_principal_dict),
            callback=cls.parse_exhibit_page, cookies=cookies)

    @classmethod
    def parse_principal_page(cls, response):
        page = PrincipalListPage(response.url, content=response.body, 
            page_context=response.meta["page_context"])
        cookies = response.headers.getlist('Cookie')
        print "\n\n\n\n\n\n\n\n\n\n\n\n\n"
        print(cookies)
        return cls._next_requests(page, cookies)

    @classmethod
    def parse_exhibit_page(cls, response):
        partial_principal_dict = response.meta["partial_principal_dict"]
        principal = ForeignPrincipal(partial_dict=partial_principal_dict)
        principal.validate_data()

        exhibit_page = ExhibitPage(response.body)
        exhibits = exhibit_page.exhibits()
        print len(response.body)
        print exhibits
        

        for exhibit in exhibits:
            print exhibit.to_dict()
            exhibit.validate()
            principal.add_exhibit_dict(exhibit.to_dict())

        full_principal_dict = principal.to_dict()
        #print("\n\n\n\n")
        #print(full_principal_dict)
        yield full_principal_dict