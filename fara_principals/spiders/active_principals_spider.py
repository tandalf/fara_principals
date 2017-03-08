import scrapy

from fara_principals.core.pages import PrincipalListPage
from fara_principals.core.principals import ForeignPrincipal

class ActivePrincipalsSpider(scrapy.Spider):
    name = 'active_principals'

    def __init__(self, *args, **kwargs):
        next_requests = []
        begin_url = 'https://efile.fara.gov/pls/apex/' + \
            'f?p=171:130:0::NO:RP,130:P130_DATERANGE:N'

        page = PrincipalListPage(begin_url)
        dict_cookies = page.main_page_cookie()
        next_page_url = page.next_page_url()
        next_page_request = scrapy.Request(url=next_page_url, 
            callback=self.parse_page)
        next_requests.append(next_page_request)

        for partial_principal in page.principals():
            principal_request = self.build_principal_request(partial_principal)
            next_requests.append(principal_request)

        return next_requests

    def build_principal_request(self, principal):
        partial_principal_dict = principal.to_dict()
        return scrapy.Request(url=partial_principal_dict["url"], 
            meta=dict(partial_principal_dict=partial_principal_dict),
            callback=self.parse_principal)

    def parse_page(self, response):
        pass

    def parse_principal(self, response):
        partial_principal_dict = response.meta["partial_principal_dict"]
        principal = ForeignPrincipal(partial_dict=partial_principal_dict)
        exibits = ExhibitsPage.exibits()

        for exhibit in exhibits:
            principal.add_exhibit_dict(exhibit.to_dict())
            yield principal.to_dict()