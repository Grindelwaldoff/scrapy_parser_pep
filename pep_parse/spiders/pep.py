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
            '//@href[starts-with(., "pep")]'
        )[1:-2]
        for pep_row_index in range(0, len(pep_rows)):
            pep_link = urljoin(
                response._url,
                pep_rows[pep_row_index].get()
            )
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        title = response.css('h1.page-title::text').get().split('–')
        for dt in response.xpath('//dl/dt'):
            if 'Status' in dt.get():
                status = dt.xpath(
                    'string(following-sibling::dd[1])'
                ).extract()[0]
        yield PepParseItem(
            {
                'name': title[1],
                'number': title[0].split()[1],
                'status': status,
            }
        )
