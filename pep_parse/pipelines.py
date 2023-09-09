# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import datetime
import csv
from collections import defaultdict

from pep_parse.settings import (
    TIME_FORMAT, SUMMARY_FILENAME,
    RESULT_DIRNAME, BASE_DIR
)


class PepParsePipeline:
    def open_spider(self, spider):
        self.statuses = defaultdict(int)

    def process_item(self, item, spider):
        self.statuses[item['status']] += 1
        print(item['status'])
        return item

    def close_spider(self, spider):
        time = datetime.datetime.now().strftime(TIME_FORMAT)
        with open(
            (f'{BASE_DIR / RESULT_DIRNAME}'
             f'/{SUMMARY_FILENAME.format(time=time)}'),
            mode='w',
            encoding='utf-8'
        ) as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['Status', 'Amount'])
            writer.writeheader()
            for key, value in self.statuses.items():
                writer.writerow({'Status': key, 'Amount': value})
            writer.writerow(
                {
                    'Status': 'Total',
                    'Amount': sum(list(self.statuses.values()))
                }
            )
