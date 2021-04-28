# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class EcommercePipeline:
    def process_item(self, item, spider):
        for k, v in item.items():
            if k == 'Regular Price':
                item[k] = "{:.2f}".format(float(v))
            if k == 'Images':
                for i in range(len(item[k])):
                    item[k][i] = "https:" + item[k][i]

        return item
