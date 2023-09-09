from urllib.parse import urljoin

import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        index_by_category_section = response.css(
            'section#index-by_category'
        )
        numerical_index_section = response.css(
            'section#numerical-index'
        )
        pep_rows = (
            index_by_category_section.css('td') + numerical_index_section.css(
                'td'
            )
        )
        for pep_row_index in range(0, len(pep_rows), 4):
            # table_status = pep_rows[pep_row_index].css('abbr::text').get()
            pep_link = urljoin(
                response._url,
                pep_rows[pep_row_index + 1].css('a::attr(href)').extract()[0]
            )
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        title = response.css('h1.page-title::text').get().split()
        for dt in response.xpath('//dl/dt'):
            if dt.css('::text').get() == 'Status':
                status = dt.xpath(
                    'string(following-sibling::dd[1])'
                ).extract()[0]
        yield PepParseItem(
            {
                'name': ' '.join(title[3:]),
                'number': title[1],
                'status': status,
            }
        )
