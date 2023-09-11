from urllib.parse import urljoin

import scrapy

from pep_parse.items import PepParseItem
from pep_parse.settings import MAIN_DOMAIN


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = [MAIN_DOMAIN]
    start_urls = [f'https://{MAIN_DOMAIN}/']

    def parse(self, response):
        pep_rows = response.xpath(
            '//td[position()=2]/a/@href[starts-with(., "pep")]'
        )
        for pep_row_index in range(0, len(pep_rows)):
            pep_link = urljoin(
                response._url,
                pep_rows[pep_row_index].get()
            )
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        pep_number, name = response.css('h1.page-title::text').get().split('–')
        status = response.xpath(
            'string(//dt[contains(text(), "Status")]/following-sibling::dd[1])'
        ).get()
        yield PepParseItem(
            {
                'name': name,
                # забираем только номер из заголовка на странице вида: PEP xxxx
                'number': pep_number.split()[1],
                'status': status,
            }
        )
