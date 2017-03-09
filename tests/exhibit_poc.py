from scrapy import Selector

def get_all_exhibit_rows(page):
    return Selector(text=page).xpath(
        '//table[@class="apexir_WORKSHEET_DATA"]/tr[@class="even"] | ' + \
        '//table[@class="apexir_WORKSHEET_DATA"]/tr[@class="odd"]')

def get_all_exhibit_dicts(page):
    exhibit_selectors = get_all_exhibit_rows(page)
    exhibit_dicts = []
    for selector in exhibit_selectors:
        date_stamped = ''.join(selector.xpath(
            './/td[@headers="DATE_STAMPED"]/text()').extract())
        document_link = ''.join(selector.xpath(
            './/td[@headers="DOCLINK"]/a/@href').extract())
        reg_number = ''.join(selector.xpath(
            './/td[@headers="REGISTRATION_NUMBER"]/text()').extract())
        registrant = ''.join(selector.xpath(
            './/td[@headers="REGISTRANT_NAME"]/text()').extract())
        document_type = ''.join(selector.xpath(
            './/td[@headers="DOCUMENT_TYPE"]/text()').extract())

        exhibit_dicts.append(dict(date_stamped=date_stamped, 
            document_link=document_link, reg_number=reg_number,
            registrant=registrant, document_type=document_type))

    return exhibit_dicts



if __name__ == "__main__":
    with open("exhibit_page1.html") as f:
        content = f.read().replace('&nbsp;', ' ')
        print(get_all_exhibit_rows(content))
        print(get_all_exhibit_dicts(content))